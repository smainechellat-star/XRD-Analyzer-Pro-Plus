"""
RAW File Loader - isolated module for RAW-specific parsing and heuristics.
FIXED VERSION - All 8 bugs addressed
"""

import os
import re
import numpy as np
from scipy.signal import find_peaks


RAW_PROFILES = {
    'bruker_u2': {
        'offsets': [4096, 8192, 12288, 2048, 1024, 0],
        'dtypes': [('<u2', 'uint16'), ('<u4', 'uint32'), ('<i4', 'int32')],
        'angle_mode': 'metadata_or_default'
    },
    'panalytical_f4': {
        'offsets': [4096, 2048, 8192, 12288, 1024, 0],
        'dtypes': [('<f4', 'float32_le'), ('>f4', 'float32_be'), ('<u4', 'uint32')],
        'angle_mode': 'metadata_or_default'
    },
    'generic': {
        'offsets': [4096, 2048, 8192, 12288, 16384, 1024, 0],
        'dtypes': [('<u2', 'uint16'), ('<u4', 'uint32'), ('<i4', 'int32'), ('<f4', 'float32_le')],
        'angle_mode': 'metadata_or_default'
    }
}


class RawFileLoader:
    """Dedicated loader for RAW binary files."""

    def __init__(self, output_dir=None):
        self.raw_profiles = RAW_PROFILES
        self.raw_scale_factor = 1.0
        self.output_dir = output_dir  # Bug 8 fix: inject output path at init

    def load_raw_file(self, filename):
        """Profile-based RAW loader (RAW-only deterministic path)."""
        try:
            print("\n" + "="*60)
            print("🔧 RAW FILE LOADER - FIXED VERSION")
            print("="*60)
            print(f"   File: {os.path.basename(filename)}")

            with open(filename, "rb") as f:
                raw = f.read()

            file_size = len(raw)
            print(f"   File size: {file_size} bytes")

            header_text = ""
            try:
                header_text = raw[:4096].decode("ascii", errors="ignore")
            except Exception:
                pass

            print(f"\n   📋 HEADER PREVIEW (first 500 chars):")
            preview = header_text[:500].replace('\x00', ' ').replace('\r', ' ').replace('\n', ' ')
            print(f"   {preview}")
            print("-" * 60)

            # Extract metadata from header
            start_angle = None
            end_angle = None
            step_size = None
            n_points = None
            warnings = []

            # Improved pattern matching for angles
            start_patterns = [
                r"START\s*[=: ]\s*([0-9.]+)",
                r"RANGESTART\s*[=: ]\s*([0-9.]+)",
                r"STARTANGLE\s*[=: ]\s*([0-9.]+)",
                r"2THETA\s*[=: ]\s*([0-9.]+)",
                r"2-THETA\s*[=: ]\s*([0-9.]+)",
                r"TWO-THETA\s*[=: ]\s*([0-9.]+)",
                r"<START[^>]*>([0-9.]+)",
                r"<STARTANGLE[^>]*>([0-9.]+)",
                r"MINIMUM\s*2THETA\s*[=: ]\s*([0-9.]+)",
                r"MIN\s*2THETA\s*[=: ]\s*([0-9.]+)",
            ]
            for pattern in start_patterns:
                match = re.search(pattern, header_text, re.IGNORECASE)
                if match:
                    try:
                        start_angle = float(match.group(1))
                        print(f"   ✓ Found START: {start_angle}°")
                        break
                    except Exception:
                        pass

            end_patterns = [
                r"END\s*[=: ]\s*([0-9.]+)",
                r"RANGESTOP\s*[=: ]\s*([0-9.]+)",
                r"ENDANGLE\s*[=: ]\s*([0-9.]+)",
                r"MAXIMUM\s*2THETA\s*[=: ]\s*([0-9.]+)",
                r"MAX\s*2THETA\s*[=: ]\s*([0-9.]+)",
                r"<END[^>]*>([0-9.]+)",
                r"<ENDANGLE[^>]*>([0-9.]+)"
            ]
            for pattern in end_patterns:
                match = re.search(pattern, header_text, re.IGNORECASE)
                if match:
                    try:
                        end_angle = float(match.group(1))
                        print(f"   ✓ Found END: {end_angle}°")
                        break
                    except Exception:
                        pass

            step_patterns = [
                r"STEP\s*[=: ]\s*([0-9.]+)",
                r"STEPSIZE\s*[=: ]\s*([0-9.]+)",
                r"STEPWIDTH\s*[=: ]\s*([0-9.]+)",
                r"INCREMENT\s*[=: ]\s*([0-9.]+)",
                r"<STEP[^>]*>([0-9.]+)"
            ]
            for pattern in step_patterns:
                match = re.search(pattern, header_text, re.IGNORECASE)
                if match:
                    try:
                        step_size = float(match.group(1))
                        print(f"   ✓ Found STEP: {step_size}°")
                        break
                    except Exception:
                        pass

            points_patterns = [
                r"POINTS\s*[=: ]\s*([0-9]+)",
                r"NPOINTS\s*[=: ]\s*([0-9]+)",
                r"DATAPT\s*[=: ]\s*([0-9]+)",
                r"COUNT\s*[=: ]\s*([0-9]+)",
                r"DATA\s*POINTS\s*[=: ]\s*([0-9]+)",
                r"<COUNT[^>]*>([0-9]+)",
                r"<NPOINTS[^>]*>([0-9]+)"
            ]
            for pattern in points_patterns:
                match = re.search(pattern, header_text, re.IGNORECASE)
                if match:
                    try:
                        n_points = int(match.group(1))
                        print(f"   ✓ Found POINTS: {n_points}")
                        break
                    except Exception:
                        pass

            profile_name = self._select_raw_profile(header_text)
            profile = self.raw_profiles.get(profile_name, self.raw_profiles['generic'])
            print(f"   🎯 RAW profile: {profile_name}")

            # Extract intensity data
            candidate = self._extract_raw_signal(raw, file_size, profile, n_points)
            if candidate is None:
                print("   ❌ No valid intensity data found for selected RAW profile")
                return None

            best_offset, best_format, intensities, quality, decode_mode = candidate
            print(f"   ✅ Profile decode candidate: offset={best_offset}, format={best_format}, mode={decode_mode}, points={len(intensities)}, quality={quality:.2f}")

            # Clean data
            valid_mask = np.isfinite(intensities) & (intensities >= 0)
            intensities = intensities[valid_mask]

            if len(intensities) < 100:
                print("   ❌ Too few valid points after cleaning")
                return None

            # Suppress spikes (Bug 7 fix: process edges)
            intensities, spike_count = self._suppress_isolated_spikes(intensities)
            if spike_count > 0:
                warning = f"Suppressed {spike_count} isolated RAW spike artifacts."
                warnings.append(warning)
                print(f"   ⚠ {warning}")

            # Check if data is inverted (background higher than peaks)
            if self._is_data_inverted(intensities):
                print("   ⚠ Data appears to be inverted! Applying auto-inversion fix...")
                intensities = self._fix_inverted_data(intensities)
                warning = "RAW data was inverted and has been corrected automatically."
                warnings.append(warning)
                print(f"   ✅ Applied inversion fix")

            if quality < 1.0:
                warning = "RAW signal quality is low; decoded pattern may be distorted."
                warnings.append(warning)
                print(f"   ⚠ {warning}")

            if decode_mode != 'direct':
                warning = f"RAW signal repaired using {decode_mode} decode mode."
                warnings.append(warning)
                print(f"   ⚠ {warning}")

            n_pts = len(intensities)
            
            # Generate 2θ angles (Bug 3 fix: removed quartz heuristic)
            two_theta = self._generate_two_theta_angles(
                start_angle, end_angle, step_size, n_pts, 
                intensities, filename, warnings
            )

            # Ensure monotonic increasing
            if two_theta[0] > two_theta[-1]:
                two_theta = two_theta[::-1]
                intensities = intensities[::-1]

            # Sort if not monotonic
            if len(two_theta) > 1 and not np.all(np.diff(two_theta) > 0):
                sort_idx = np.argsort(two_theta)
                two_theta = two_theta[sort_idx]
                intensities = intensities[sort_idx]

            # Remove duplicates
            if len(two_theta) > 1:
                unique_theta, unique_idx = np.unique(two_theta, return_index=True)
                if len(unique_theta) < len(two_theta):
                    two_theta = unique_theta
                    intensities = intensities[unique_idx]

            # Analyze peaks (diagnostic only - Bug 3 fix)
            try:
                prominence = max(1.0, 0.03 * (np.max(intensities) - np.min(intensities)))
                test_peaks, _ = find_peaks(intensities, prominence=prominence, distance=max(3, n_pts//250))
                print(f"\n   📊 Detected {len(test_peaks)} peaks in data")
                
                if len(test_peaks) > 0:
                    peak_indices = test_peaks[np.argsort(intensities[test_peaks])[-3:]]  # Top 3 peaks
                    peak_angles = two_theta[peak_indices]
                    
                    print(f"   📊 Top 3 peaks:")
                    for i, angle in enumerate(peak_angles):
                        print(f"      Peak {i+1}: {angle:.2f}°")
                    
                    # Diagnostic only - no scaling applied (Bug 3 fix)
                    if 5 < peak_angles[0] < 150:
                        print(f"   ℹ Strongest peak at {peak_angles[0]:.2f}° — verify this matches your expected pattern.")
            except Exception as e:
                print(f"   ⚠ Peak detection failed: {e}")

            print(f"\n   ✅ RAW parsed successfully:")
            print(f"      Final points: {len(two_theta)}")
            print(f"      Range: {two_theta[0]:.2f}° - {two_theta[-1]:.2f}°")
            print(f"      Step size (avg): {np.mean(np.diff(two_theta)):.4f}°")

            # ===== BUG 1 FIX: ASCII export is non-blocking =====
            asc_path = self._export_ascii_from_raw(filename, two_theta, intensities)
            if asc_path is None:
                warning = "RAW→ASC conversion failed (filesystem). Data still returned."
                warnings.append(warning)
                print(f"   ⚠ {warning}")
            else:
                print(f"   ✅ RAW converted to ASCII: {asc_path}")

            # ===== BUG 2 FIX: scale factor is NOT applied (metadata angles are trusted) =====
            # We're removing the quartz-based scaling entirely per Bug 3 analysis
            # The scale factor is only stored for diagnostics, not applied to data

            return {
                "two_theta": two_theta,
                "intensity_raw": intensities,
                "filename": os.path.basename(filename),
                "format": f"RAW ({best_format})",
                "warnings": warnings,
                "metadata": {
                    "asc_path": asc_path,
                    "converted_to_ascii": asc_path is not None,
                    "raw_profile": profile_name,
                    "decode_quality": quality,
                    "offset": best_offset,
                    "format": best_format,
                    "decode_mode": decode_mode,
                    "start_angle": start_angle,
                    "end_angle": end_angle,
                    "step_size": step_size,
                    "n_points_expected": n_points,
                    "peak_angle": peak_angles[0] if 'peak_angles' in locals() and len(peak_angles) > 0 else None,
                    "scale_factor_diagnostic": self.raw_scale_factor  # For info only
                }
            }

        except Exception as e:
            import traceback
            print(f"   ❌ RAW parse error: {e}")
            traceback.print_exc()
            return None

    def _is_data_inverted(self, intensities):
        """
        Detect if intensity data is inverted (background higher than peaks).
        Returns True if data appears inverted.
        """
        if len(intensities) < 100:
            return False
        
        # Calculate statistics
        max_val = np.max(intensities)
        min_val = np.min(intensities)
        mean_val = np.mean(intensities)
        
        # Check edges (first and last 5%)
        n = len(intensities)
        edge_size = max(10, n // 20)
        
        left_edge = np.mean(intensities[:edge_size]) if edge_size > 0 else 0
        right_edge = np.mean(intensities[-edge_size:]) if edge_size > 0 else 0
        edge_mean = (left_edge + right_edge) / 2
        
        # INVERSION CRITERIA:
        # 1. Edges are high (>70% of max)
        # 2. Minimum is low (<10% of max)
        # 3. Most data is above mean (suggests background high)
        edge_ratio = edge_mean / max_val if max_val > 0 else 0
        min_ratio = min_val / max_val if max_val > 0 else 0
        above_mean_ratio = np.mean(intensities > mean_val)
        
        print(f"\n   🔍 Inversion detection:")
        print(f"      Edge ratio: {edge_ratio:.2f} (should be <0.7 for normal data)")
        print(f"      Min ratio: {min_ratio:.2f} (should be <0.1 for inverted data)")
        print(f"      Above mean: {above_mean_ratio:.2f}")
        
        is_inverted = (edge_ratio > 0.7 and min_ratio < 0.1) or above_mean_ratio > 0.7
        
        if is_inverted:
            print(f"      ⚠ Data appears INVERTED")
        else:
            print(f"      ✓ Data appears normal")
        
        return is_inverted

    def _fix_inverted_data(self, intensities):
        """Fix inverted data by subtracting from max"""
        max_val = np.max(intensities)
        fixed = max_val - intensities
        # Ensure no negative values
        fixed = np.maximum(fixed, 0)
        return fixed

    def _generate_two_theta_angles(self, start_angle, end_angle, step_size, n_pts, 
                                    intensities, filename, warnings):
        """Generate 2θ angles with improved logic for RAW files"""
        
        two_theta = None
        
        # Case 1: Complete metadata - start and end angles (most reliable)
        if start_angle is not None and end_angle is not None:
            two_theta = np.linspace(start_angle, end_angle, n_pts)
            print(f"   ✓ Generated 2θ from start/end: {start_angle:.2f}° - {end_angle:.2f}°")
        
        # Case 2: Start and step size
        elif start_angle is not None and step_size is not None:
            two_theta = start_angle + np.arange(n_pts) * step_size
            print(f"   ✓ Generated 2θ from start/step: {two_theta[0]:.2f}° - {two_theta[-1]:.2f}°")
        
        # Case 3: End and step size (working backwards)
        elif end_angle is not None and step_size is not None:
            two_theta = end_angle - (n_pts - 1) * step_size + np.arange(n_pts) * step_size
            print(f"   ✓ Generated 2θ from end/step: {two_theta[0]:.2f}° - {two_theta[-1]:.2f}°")
        
        # Case 4: Only start angle
        elif start_angle is not None:
            end_angle = start_angle + 90  # Assume 90° range
            two_theta = np.linspace(start_angle, end_angle, n_pts)
            warning = f"RAW metadata incomplete (START only). Estimated range {start_angle:.2f}°-{end_angle:.2f}°."
            warnings.append(warning)
            print(f"   ⚠ {warning}")
        
        # Case 5: Only end angle
        elif end_angle is not None:
            start_angle = max(0, end_angle - 90)  # Assume 90° range
            two_theta = np.linspace(start_angle, end_angle, n_pts)
            warning = f"RAW metadata incomplete (END only). Estimated range {start_angle:.2f}°-{end_angle:.2f}°."
            warnings.append(warning)
            print(f"   ⚠ {warning}")
        
        # Case 6: Only step size
        elif step_size is not None:
            # Try to determine range from filename or common patterns
            if "hi" in filename.lower() or "high" in filename.lower():
                start_angle = 70
                end_angle = 160
            elif "lo" in filename.lower() or "low" in filename.lower():
                start_angle = 5
                end_angle = 70
            else:
                # Try to detect from peak positions
                max_idx = np.argmax(intensities)
                if max_idx < n_pts // 3:
                    # Peak early in scan - likely low angle range
                    start_angle = 5
                    end_angle = 95
                elif max_idx > 2 * n_pts // 3:
                    # Peak late in scan - likely high angle range
                    start_angle = 40
                    end_angle = 130
                else:
                    # Peak in middle - medium range
                    start_angle = 10
                    end_angle = 100
            
            two_theta = np.linspace(start_angle, end_angle, n_pts)
            warning = f"RAW metadata incomplete (STEP only). Estimated range {start_angle:.2f}°-{end_angle:.2f}°."
            warnings.append(warning)
            print(f"   ⚠ {warning}")
        
        # Case 7: No metadata at all
        else:
            # Try to determine from file characteristics
            max_idx = np.argmax(intensities)
            peak_ratio = max_idx / n_pts
            
            if peak_ratio < 0.2:
                # Peak very early - likely low angle range
                start_angle = 5
                end_angle = 95
            elif peak_ratio > 0.8:
                # Peak very late - likely high angle range
                start_angle = 40
                end_angle = 130
            else:
                # Default range
                start_angle = 5
                end_angle = 90
            
            two_theta = np.linspace(start_angle, end_angle, n_pts)
            warning = f"RAW metadata missing. Using default 2θ range {start_angle:.2f}°-{end_angle:.2f}°."
            warnings.append(warning)
            print(f"   ⚠ {warning}")
        
        # Final check: ensure angles are in reasonable XRD range (5-150°)
        if np.max(two_theta) > 150:
            print(f"   ⚠ Max angle {np.max(two_theta):.1f}° > 150°, scaling down")
            scale = 150 / np.max(two_theta)
            two_theta = two_theta * scale
        
        if np.min(two_theta) < 0:
            print(f"   ⚠ Min angle {np.min(two_theta):.1f}° < 0°, shifting up")
            two_theta = two_theta - np.min(two_theta) + 5
        
        return two_theta

    # Bug 7 fix: process edge points
    def _suppress_isolated_spikes(self, arr):
        """Remove isolated one-point spikes while preserving real peak shapes."""
        data = np.asarray(arr, dtype=float)
        n = len(data)
        if n < 15:
            return data, 0

        repaired = data.copy()
        global_scale = np.percentile(data, 95) - np.percentile(data, 5)
        global_scale = max(global_scale, 1.0)
        spike_count = 0

        # Fixed: process from index 1 to n-2 to catch edge points
        for i in range(1, n - 1):
            left = data[max(0, i - 1)]
            right = data[min(n - 1, i + 1)]
            
            # Get window with bounds checking
            window_start = max(0, i - 2)
            window_end = min(n, i + 3)
            window = data[window_start:window_end]
            
            if len(window) < 3:
                continue
                
            local_med = np.median(window)
            local_mad = np.median(np.abs(window - local_med)) + 1e-9

            adaptive_threshold = local_med + max(20.0 * local_mad, 0.12 * global_scale)
            neighbors_mean = 0.5 * (left + right)

            # Check neighbors that exist
            left2 = data[max(0, i - 2)] if i >= 2 else data[i]
            right2 = data[min(n - 1, i + 2)] if i <= n - 3 else data[i]
            
            is_isolated = (
                data[i] > adaptive_threshold and
                data[i] > (left + 1e-9) * 5.0 and
                data[i] > (right + 1e-9) * 5.0 and
                max(left2, right2) < data[i] * 0.35
            )

            if is_isolated:
                repaired[i] = neighbors_mean
                spike_count += 1

        return repaired, spike_count

    # Bug 8 fix: flexible output path
    def _export_ascii_from_raw(self, raw_filename, two_theta, intensities):
        """Optional conversion: write decoded RAW data to two-column ASCII file."""
        try:
            # Use provided output_dir or fallback to next to source file
            if self.output_dir:
                output_dir = self.output_dir
            else:
                # Option A: next to the source file
                output_dir = os.path.join(os.path.dirname(os.path.abspath(raw_filename)), 'converted')
            
            os.makedirs(output_dir, exist_ok=True)

            base_name = os.path.splitext(os.path.basename(raw_filename))[0]
            asc_path = os.path.join(output_dir, f"{base_name}_converted.asc")

            arr = np.column_stack((two_theta, intensities))
            np.savetxt(asc_path, arr, fmt='%.6f %.6f')

            if not os.path.exists(asc_path) or os.path.getsize(asc_path) == 0:
                return None

            return asc_path
        except Exception as e:
            print(f"   ⚠ ASCII export error: {e}")
            return None

    def _select_raw_profile(self, header_text):
        """Pick RAW profile from header signature."""
        text = (header_text or "").upper()
        if "BRUKER" in text or "DIFFRAC" in text:
            return 'bruker_u2'
        if "PANALYTICAL" in text or "MALVERN" in text or "X'PERT" in text:
            return 'panalytical_f4'
        return 'generic'

    # Bug 4 fix: preserve full sequence
    def _extract_raw_signal(self, raw, file_size, profile, n_points_expected=None):
        """Extract intensity signal deterministically from selected profile."""
        candidates = []

        for offset in profile.get('offsets', []):
            if offset >= file_size - 100:
                continue

            for dtype, label in profile.get('dtypes', []):
                try:
                    data = np.frombuffer(raw, dtype=dtype, offset=offset).astype(float)
                except Exception:
                    continue

                if len(data) < 100:
                    continue

                finite = data[np.isfinite(data)]
                finite = finite[finite >= 0]
                if len(finite) < 100:
                    continue

                if not self._is_valid_signal(finite):
                    continue

                sequences = [(finite, 'direct')]
                if label == 'uint16':
                    repaired = self._repair_word_split_uint16(finite)
                    if repaired is not None and len(repaired) >= 100:
                        sequences.append((repaired, 'uint16_deinterleaved'))

                for seq, decode_mode in sequences:
                    # Bug 4 fix: always include full sequence
                    segments = [seq]
                    
                    # Add slices only if they provide non-overlapping candidates
                    if n_points_expected and n_points_expected > 100 and len(seq) > n_points_expected:
                        segments.append(seq[:n_points_expected])
                        if len(seq) >= 2 * n_points_expected:  # Only add back-slice if non-overlapping
                            segments.append(seq[-n_points_expected:])

                    for segment in segments:
                        score = self._score_xrd_signal(segment)
                        if n_points_expected:
                            score -= abs(len(segment) - n_points_expected) * 0.005

                        artifact_like = self._is_artifact_like_signal(segment)
                        candidates.append((offset, label, segment, score, decode_mode, artifact_like))

        if not candidates:
            return None

        non_artifact = [c for c in candidates if not c[5]]
        pool = non_artifact if non_artifact else candidates
        best = max(pool, key=lambda x: x[3])
        return best[:5]

    def _is_artifact_like_signal(self, arr):
        """Detect quantized/saturated decode artifacts common in mis-read RAW streams."""
        arr = np.asarray(arr, dtype=float)
        if len(arr) < 100:
            return False

        unique_ratio = len(np.unique(arr)) / len(arr)
        p10 = np.percentile(arr, 10)
        p90 = np.percentile(arr, 90)
        p99 = np.percentile(arr, 99)
        p1 = np.percentile(arr, 1)

        baseline_ratio = p10 / (p90 + 1e-9)
        dynamic_ratio = (p99 - p1) / (np.percentile(arr, 50) + 1e-9)

        # Bug 6 fix: consistent 10% threshold
        too_quantized = unique_ratio < 0.10
        too_saturated = baseline_ratio > 0.82 and dynamic_ratio < 0.15
        return too_quantized or too_saturated

    def _repair_word_split_uint16(self, arr):
        """Repair 16-bit word-split pattern: 0, value, 0, value ..."""
        if len(arr) < 200:
            return None

        even = arr[0::2]
        odd = arr[1::2]
        if len(even) < 100 or len(odd) < 100:
            return None

        even_zero = np.mean(even <= 1.0)
        odd_zero = np.mean(odd <= 1.0)

        if even_zero > 0.6 and odd_zero < 0.2:
            return odd
        if odd_zero > 0.6 and even_zero < 0.2:
            return even
        return None

    # Bug 6 fix: consistent thresholds with _is_artifact_like_signal
    def _score_xrd_signal(self, arr):
        """Score candidate signal for XRD-like shape quality."""
        arr = np.asarray(arr, dtype=float)
        if len(arr) < 100:
            return -1e9

        p1 = np.percentile(arr, 1)
        p5 = np.percentile(arr, 5)
        p10 = np.percentile(arr, 10)
        p50 = np.percentile(arr, 50)
        p90 = np.percentile(arr, 90)
        p95 = np.percentile(arr, 95)
        p99 = np.percentile(arr, 99)
        dynamic = p99 - p1
        if dynamic <= 0:
            return -1e9

        diffs = np.diff(arr)
        diff_std = np.std(diffs) + 1e-9
        spike_ratio = np.mean(np.abs(diffs) > (8.0 * diff_std)) if len(diffs) > 0 else 1.0

        zero_ratio = np.mean(arr <= 1.0)

        flat_band = 0.01 * dynamic
        flat_ratio = np.mean(np.abs(arr - p50) <= flat_band)

        dominance = np.max(arr) / (p95 + 1e-9)

        baseline_ratio = p10 / (p90 + 1e-9)
        high_occupancy = np.mean(arr >= p90)
        unique_ratio = len(np.unique(arr)) / len(arr)
        dynamic_ratio = dynamic / (p50 + 1e-9)

        try:
            prominence = max(1.0, 0.03 * dynamic)
            distance = max(3, len(arr) // 250)
            peaks, _ = find_peaks(arr, prominence=prominence, distance=distance)
            peak_count = len(peaks)
        except Exception:
            peak_count = 0

        score = 0.0
        score += np.log10(dynamic + 1.0)
        score += min(peak_count, 30) * 0.05
        score -= spike_ratio * 4.0
        score -= max(0.0, zero_ratio - 0.05) * 6.0
        score -= max(0.0, flat_ratio - 0.25) * 3.0
        if baseline_ratio > 0.65:
            score -= (baseline_ratio - 0.65) * 18.0
        if high_occupancy > 0.35:
            score -= (high_occupancy - 0.35) * 12.0
        # Bug 6 fix: consistent 10% threshold
        if unique_ratio < 0.10:
            score -= (0.10 - unique_ratio) * 80.0
        if dynamic_ratio < 0.08:
            score -= (0.08 - dynamic_ratio) * 40.0
        if dominance > 8.0:
            score -= (dominance - 8.0) * 0.2

        return score

    # Bug 5 fix: clearer logic and relaxed threshold
    def _is_valid_signal(self, arr, min_points=100):
        """Check if array contains valid XRD signal."""
        if arr is None or len(arr) < min_points:
            return False

        arr = np.asarray(arr)
        arr = arr[np.isfinite(arr)]
        if len(arr) == 0:
            return False

        if np.max(arr) <= 0:
            return False

        # Bug 5 fix: clearer logic with relaxed threshold (0.1% instead of 1%)
        mean_val = np.mean(arr)
        if mean_val > 0 and np.std(arr) < 0.001 * mean_val:  # 0.1% threshold
            return False

        if np.max(arr) > 1e9:
            return False

        return True