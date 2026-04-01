"""
Universal XRD File Loader - RAW-focused correction strategy
"""

import os
import re
import numpy as np
import xml.etree.ElementTree as ET
import struct
from processing.raw_loader import RawFileLoader

class XRDFileLoader:
    """Universal XRD file loader with format-specific parsers"""

    def __init__(self):
        self.wavelength = 1.5406
        self.raw_loader = RawFileLoader()
        print("🔧 XRDFileLoader initialized")

    def load_file(self, filename):
        """Load any XRD file with automatic format detection"""
        if not os.path.exists(filename):
            print(f"❌ File not found: {filename}")
            return None

        ext = os.path.splitext(filename)[1].lower()
        print(f"\n📂 Loading file: {os.path.basename(filename)}")
        print(f"   Extension: {ext}")

        handlers = {
            '.xrdml': self._load_xrdml,
            '.raw': self._load_raw,
            '.ras': self._load_ras,
            '.rd': self._load_txt,
            '.csv': self._load_csv,
            '.txt': self._load_txt,
            '.dat': self._load_dat,
            '.asc': self._load_ascii,
            '.xy': self._load_ascii,
        }

        data = None
        if ext in handlers:
            data = handlers[ext](filename)
        else:
            data = self._load_ascii(filename)

        if data is None:
            print(f"❌ Could not parse {ext} format")
            return None

        validated = self._validate_and_correct(data, filename)
        if validated is None:
            return None

        if isinstance(data, dict) and data.get('warnings'):
            existing = validated.get('warnings', [])
            if validated is data:
                merged = existing
            else:
                merged = existing + data.get('warnings', [])
            validated['warnings'] = list(dict.fromkeys(merged))

        return validated

    # ===== XRDML PARSER =====
    def _load_xrdml(self, filename):
        """Load XRDML format"""
        try:
            print("   Parsing as XRDML...")
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Remove namespaces to simplify parsing
            content = re.sub(r'xmlns="[^"]+"', '', content)
            root = ET.fromstring(content)

            two_theta = None
            intensity = None

            # Try direct positions list
            positions = root.find('.//positions')
            if positions is not None and positions.text:
                pos_values = list(map(float, positions.text.strip().split()))
                if len(pos_values) > 10:
                    two_theta = np.array(pos_values, dtype=float)
                    print(f"   ✓ Found positions: {len(pos_values)} points")

            # Try intensities
            intensities = root.find('.//intensities')
            if intensities is not None and intensities.text:
                int_values = list(map(float, intensities.text.strip().split()))
                intensity = np.array(int_values, dtype=float)
                print(f"   ✓ Found intensities: {len(int_values)} points")

            # Fallback: Start/End/Count pattern
            if two_theta is None and intensity is not None:
                start = root.find('.//startPosition')
                end = root.find('.//endPosition')
                
                if start is not None and end is not None:
                    start_val = float(start.text)
                    end_val = float(end.text)
                    two_theta = np.linspace(start_val, end_val, len(intensity))
                    print(f"   ✓ Generated 2θ from start/end: {start_val}° - {end_val}°")

            if two_theta is None or intensity is None:
                print("   ❌ Could not extract both 2θ and intensity")
                return None

            # Ensure same length
            min_len = min(len(two_theta), len(intensity))
            two_theta = two_theta[:min_len]
            intensity = intensity[:min_len]

            return {
                'two_theta': two_theta,
                'intensity_raw': intensity,
                'filename': os.path.basename(filename),
                'format': 'XRDML'
            }
        except Exception as e:
            print(f"   ❌ XRDML parse error: {e}")
            return None

    # ===== RAW PARSER =====
    def _load_raw(self, filename):
        """Delegate RAW parsing to dedicated module."""
        return self.raw_loader.load_raw_file(filename)

    # ===== RAS PARSER (Rigaku) =====
    def _load_ras(self, filename):
        """Load Rigaku RAS format"""
        try:
            print("   Parsing as RAS...")
            with open(filename, 'rb') as f:
                data = f.read()

            int_vals = []
            for i in range(0, len(data)-1, 2):
                try:
                    val = struct.unpack('<H', data[i:i+2])[0]
                    int_vals.append(float(val))
                except:
                    pass

            if len(int_vals) > 100:
                print(f"   ✓ Found {len(int_vals)} data points")
                two_theta = np.linspace(5, 90, len(int_vals))
                return {
                    'two_theta': two_theta,
                    'intensity_raw': np.array(int_vals),
                    'filename': os.path.basename(filename),
                    'format': 'RAS (Rigaku)'
                }
            return None
        except Exception as e:
            print(f"   ❌ RAS parse error: {e}")
            return None

    # ===== CSV PARSER =====
    def _load_csv(self, filename):
        """Load CSV data"""
        try:
            print("   Parsing as CSV...")
            data = np.loadtxt(filename, delimiter=',')
            
            if data.ndim == 1:
                two_theta = np.linspace(5, 90, len(data))
                intensity = data
            else:
                two_theta = data[:, 0]
                intensity = data[:, 1]
            
            return {
                'two_theta': np.array(two_theta, dtype=float),
                'intensity_raw': np.array(intensity, dtype=float),
                'filename': os.path.basename(filename),
                'format': 'CSV'
            }
        except Exception as e:
            print(f"   ❌ CSV parse error: {e}")
            return self._load_ascii(filename)

    # ===== TXT/DAT/ASCII PARSER =====
    def _load_txt(self, filename):
        return self._load_ascii(filename)

    def _load_dat(self, filename):
        return self._load_ascii(filename)

    def _load_ascii(self, filename):
        """Load generic ASCII data (space-separated)"""
        try:
            print("   Parsing as ASCII...")
            data = np.loadtxt(filename)
            
            if data.ndim == 1:
                two_theta = np.linspace(5, 90, len(data))
                intensity = data
            else:
                two_theta = data[:, 0]
                intensity = data[:, 1]

            return {
                'two_theta': np.array(two_theta, dtype=float),
                'intensity_raw': np.array(intensity, dtype=float),
                'filename': os.path.basename(filename),
                'format': 'ASCII'
            }
        except Exception as e:
            print(f"   ❌ ASCII parse error: {e}")
            return None

    # ===== SIGNAL VALIDATION =====
    def _is_valid_signal(self, arr, min_points=100):
        """Check if array contains valid XRD signal"""
        if arr is None or len(arr) < min_points:
            return False

        arr = np.asarray(arr)
        arr = arr[np.isfinite(arr)]
        if len(arr) == 0:
            return False

        if np.max(arr) <= 0:
            return False

        if np.std(arr) < 0.01 * np.mean(arr) if np.mean(arr) > 0 else False:
            return False

        if np.max(arr) > 1e9:
            return False

        return True

    # ===== VALIDATION AND CORRECTION =====
    def _validate_and_correct(self, data, filename):
        """Validate and apply corrections (RAW inversion only)"""
        if data is None:
            return None

        two_theta = np.array(data['two_theta'], dtype=float)
        intensity = np.array(data['intensity_raw'], dtype=float)

        min_len = min(len(two_theta), len(intensity))
        two_theta = two_theta[:min_len]
        intensity = intensity[:min_len]

        mask = np.isfinite(two_theta) & np.isfinite(intensity)
        two_theta = two_theta[mask]
        intensity = intensity[mask]

        if len(two_theta) == 0:
            print("❌ No valid data points after cleaning")
            return None

        sort_idx = np.argsort(two_theta)
        two_theta = two_theta[sort_idx]
        intensity = intensity[sort_idx]

        _, uniq_idx = np.unique(two_theta, return_index=True)
        if len(uniq_idx) < len(two_theta):
            two_theta = two_theta[uniq_idx]
            intensity = intensity[uniq_idx]

        is_raw_file = str(filename).lower().endswith('.raw') or 'raw' in str(data.get('format', '')).lower()
        if is_raw_file:
            print(f"\n🔍 Checking for inverted RAW data...")

            min_int = np.min(intensity)
            max_int = np.max(intensity)
            mean_int = np.mean(intensity)

            n = len(intensity)
            edge_size = max(10, n // 20)

            left_edge = np.mean(intensity[:edge_size]) if len(intensity[:edge_size]) > 0 else 0
            right_edge = np.mean(intensity[-edge_size:]) if len(intensity[-edge_size:]) > 0 else 0
            edge_mean = (left_edge + right_edge) / 2

            print(f"   Intensity stats - Min: {min_int:.2f}, Max: {max_int:.2f}, Mean: {mean_int:.2f}")
            print(f"   Edge average: {edge_mean:.2f}")

            edge_ratio = edge_mean / max_int if max_int > 0 else 0
            min_ratio = min_int / max_int if max_int > 0 else 0

            print(f"   Edge/Max ratio: {edge_ratio:.3f}")
            print(f"   Min/Max ratio: {min_ratio:.3f}")

            if edge_ratio > 0.7 and min_ratio < 0.1:
                print(f"   ⚠ INVERTED RAW DATA DETECTED - Applying inversion: I = max - I")
                intensity = max_int - intensity
                print(f"      After inversion - Min: {np.min(intensity):.2f}, Max: {np.max(intensity):.2f}")
            else:
                print(f"   ✓ RAW data appears correctly oriented")
        else:
            print(f"\n🔍 Skipping inversion correction for non-RAW format: {data.get('format', 'Unknown')}")

        print(f"\n🔍 Validated data:")
        print(f"   Points: {len(two_theta)}")
        print(f"   2θ range: {two_theta[0]:.2f}° - {two_theta[-1]:.2f}°")
        print(f"   Intensity range: {np.min(intensity):.0f} - {np.max(intensity):.0f}")

        if len(intensity) > 0:
            max_idx = np.argmax(intensity)
            peak_angle = two_theta[max_idx]
            print(f"   Strongest peak at: {peak_angle:.2f}°")

        data['two_theta'] = two_theta
        data['intensity_raw'] = intensity
        return data