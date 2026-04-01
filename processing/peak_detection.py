"""
PROFESSIONAL XRD PEAK DETECTION
WITH COMPLETE PREPROCESSING PIPELINE - ENHANCED VERSION
Includes database matching for mineral labels
"""

import numpy as np
from scipy.signal import savgol_filter, find_peaks
from scipy.ndimage import gaussian_filter1d
import sqlite3
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

class XRDConverter:
    """Simple converter for 2θ to d-spacing"""
    
    def __init__(self, wavelength=1.5406):
        self.wavelength = wavelength
    
    def two_theta_to_d(self, two_theta):
        """Convert 2θ (degrees) to d-spacing (Å) using Bragg's Law"""
        two_theta = np.array(two_theta, dtype=float)
        theta = two_theta / 2.0
        theta_rad = np.radians(theta)
        sin_theta = np.sin(theta_rad)
        # Avoid division by zero
        sin_theta = np.where(np.abs(sin_theta) < 1e-10, 1e-10, sin_theta)
        return self.wavelength / (2.0 * sin_theta)
    
    def d_to_two_theta(self, d_spacing):
        """Convert d-spacing (Å) to 2θ (degrees)"""
        d_spacing = np.array(d_spacing, dtype=float)
        sin_theta = self.wavelength / (2.0 * d_spacing)
        # Clip to valid range
        sin_theta = np.clip(sin_theta, -1, 1)
        theta_rad = np.arcsin(sin_theta)
        theta = np.degrees(theta_rad)
        return 2.0 * theta


class PeakDetector:
    """Professional XRD peak detector with proper preprocessing and mineral labeling"""
    
    def __init__(self, wavelength=1.5406, db_path=None):
        self.wavelength = wavelength
        self.converter = XRDConverter(wavelength=wavelength)
        self.db_path = db_path or self._find_database()
        self.db_connection = None
        self._minerals_columns = None
        
    def _find_database(self):
        """Find the COD database file"""
        possible_paths = [
            r"D:\Project XRD Analyzer\XRD-Analyzer Pro\xrd-analyzer-pro\assets\cod_xrd_final.db",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "cod_xrd_final.db"),
            os.path.join(os.getcwd(), "assets", "cod_xrd_final.db"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ Found database: {path}")
                return path
        
        print("⚠️ Database not found - peaks will be unlabeled")
        return None
    
    def connect_db(self):
        """Establish database connection"""
        if self.db_path and os.path.exists(self.db_path):
            try:
                self.db_connection = sqlite3.connect(self.db_path)
                self.db_connection.row_factory = sqlite3.Row
                return True
            except Exception as e:
                print(f"⚠️ Database connection error: {e}")
        return False
    
    def close_db(self):
        """Close database connection"""
        if self.db_connection:
            self.db_connection.close()
            self.db_connection = None

    def _get_minerals_columns(self):
        """Get available columns in minerals table (cached)."""
        if self._minerals_columns is not None:
            return self._minerals_columns

        if not self.db_connection and not self.connect_db():
            self._minerals_columns = set()
            return self._minerals_columns

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("PRAGMA table_info(minerals)")
            self._minerals_columns = {row[1] for row in cursor.fetchall()}
        except Exception:
            self._minerals_columns = set()

        return self._minerals_columns

    def _first_existing_column(self, candidates):
        """Return first existing column name from candidates."""
        cols = self._get_minerals_columns()
        for col in candidates:
            if col in cols:
                return col
        return None
    
    def match_peak_with_database(self, d_spacing, tolerance=0.02):
        """
        Match a single peak with database minerals
        Returns list of potential matches with names and formulas
        """
        if not self.db_connection and not self.connect_db():
            return []
        
        try:
            cursor = self.db_connection.cursor()

            name_col = self._first_existing_column([
                'substance_name', 'mineral_name', 'name', 'phase_name', 'label'
            ])
            formula_col = self._first_existing_column([
                'chemical_formula', 'formula'
            ])
            category_col = self._first_existing_column([
                'category', 'mineral_group', 'group_name'
            ])

            if not name_col:
                return []

            formula_expr = f"COALESCE({formula_col}, '') AS formula" if formula_col else "'' AS formula"
            category_expr = f"COALESCE({category_col}, '') AS category" if category_col else "'' AS category"
            
            # Search across first 5 d-spacing columns
            query = """
            SELECT {name_col} AS mineral_name, {formula_expr}, {category_expr},
                   d1, i1, d2, i2, d3, i3, d4, i4, d5, i5,
                   ABS(d1 - ?) as diff1,
                   ABS(d2 - ?) as diff2,
                   ABS(d3 - ?) as diff3,
                   ABS(d4 - ?) as diff4,
                   ABS(d5 - ?) as diff5
            FROM minerals 
            WHERE (ABS(d1 - ?) <= ? OR 
                   ABS(d2 - ?) <= ? OR 
                   ABS(d3 - ?) <= ? OR 
                   ABS(d4 - ?) <= ? OR 
                   ABS(d5 - ?) <= ?)
            AND {name_col} IS NOT NULL
            AND {name_col} != ''
            ORDER BY 
                MIN(
                    IFNULL(ABS(d1 - ?), 999),
                    IFNULL(ABS(d2 - ?), 999),
                    IFNULL(ABS(d3 - ?), 999),
                    IFNULL(ABS(d4 - ?), 999),
                    IFNULL(ABS(d5 - ?), 999)
                ) ASC,
                i1 DESC
            LIMIT 3
            """

            query = query.format(
                name_col=name_col,
                formula_expr=formula_expr,
                category_expr=category_expr
            )
            
            cursor.execute(query, (d_spacing, d_spacing, d_spacing, d_spacing, d_spacing,
                                   d_spacing, tolerance, d_spacing, tolerance, 
                                   d_spacing, tolerance, d_spacing, tolerance,
                                   d_spacing, tolerance,
                                   d_spacing, d_spacing, d_spacing, d_spacing, d_spacing))
            
            matches = cursor.fetchall()
            result = []
            
            for match in matches:
                # Find which column matched and the difference
                diffs = [
                    (match['diff1'] if match['diff1'] is not None else 999, 1),
                    (match['diff2'] if match['diff2'] is not None else 999, 2),
                    (match['diff3'] if match['diff3'] is not None else 999, 3),
                    (match['diff4'] if match['diff4'] is not None else 999, 4),
                    (match['diff5'] if match['diff5'] is not None else 999, 5)
                ]
                best_diff, best_col = min(diffs, key=lambda x: x[0])
                
                if best_diff <= tolerance:
                    result.append({
                        'name': match['mineral_name'],
                        'formula': match['formula'] or '',
                        'category': match['category'] or '',
                        'mineral_group': match['category'] or '',
                        'matched_d': match[f'd{best_col}'],
                        'matched_i': match[f'i{best_col}'],
                        'delta': best_diff,
                        'quality': 'excellent' if best_diff < 0.01 else 'good'
                    })
            
            return result
            
        except Exception as e:
            print(f"⚠️ Database query error: {e}")
            return []
    
    def preprocess(self, intensity, smoothing_window=11):
        """
        COMPLETE PREPROCESSING PIPELINE
        Step 1: Smoothing (Savitzky-Golay)
        Step 2: Baseline removal
        """
        # Ensure smoothing_window is odd
        if smoothing_window % 2 == 0:
            smoothing_window += 1
        if smoothing_window < 5:
            smoothing_window = 5
        if smoothing_window > len(intensity) // 5:
            smoothing_window = max(5, len(intensity) // 10)
            if smoothing_window % 2 == 0:
                smoothing_window += 1
        
        try:
            # STEP 1: SAVITZKY-GOLAY SMOOTHING
            intensity_smooth = savgol_filter(
                intensity, 
                window_length=smoothing_window, 
                polyorder=3,
                mode='interp'
            )
        except:
            # Fallback to Gaussian smoothing
            sigma = smoothing_window / 5.0
            intensity_smooth = gaussian_filter1d(intensity, sigma=sigma)
        
        # STEP 2: BASELINE REMOVAL
        baseline = np.min(intensity_smooth)
        intensity_corrected = intensity_smooth - baseline
        
        # Ensure no negative values
        intensity_corrected = np.maximum(intensity_corrected, 0)
        
        return intensity_corrected, baseline
    
    def detect_peaks(self, two_theta, intensity, 
                    prominence_factor=1.5,
                    min_distance=0.5,
                    min_width=0.2,
                    smoothing_window=7,
                    min_intensity_percent=1.0,
                    match_with_db=True):
        """
        COMPLETE PEAK DETECTION PIPELINE
        Returns peaks with d-spacings, intensities, and mineral labels
        """
        
        # Convert inputs to numpy arrays
        two_theta = np.array(two_theta, dtype=float)
        intensity = np.array(intensity, dtype=float)
        
        # ========== STEP 1: PREPROCESSING ==========
        intensity_processed, baseline = self.preprocess(
            intensity, 
            smoothing_window
        )
        
        # ========== STEP 2: ESTIMATE NOISE LEVEL ==========
        n_points = len(intensity_processed)
        n_noise = max(10, n_points // 20)
        
        noise_region1 = intensity_processed[:n_noise]
        noise_region2 = intensity_processed[-n_noise:]
        noise_region = np.concatenate([noise_region1, noise_region2])
        
        noise_std = np.std(noise_region)
        noise_mean = np.mean(noise_region)
        
        # ========== STEP 3: ADAPTIVE THRESHOLDS ==========
        prominence_threshold = max(0.5, noise_std * prominence_factor)
        height_threshold = max(0.0, noise_mean + noise_std * 2)
        
        # Convert distances from degrees to indices
        if len(two_theta) > 1:
            step_size = two_theta[1] - two_theta[0]
            distance_indices = max(1, int(min_distance / step_size))
            width_indices = max(1, int(min_width / step_size))
        else:
            distance_indices = 1
            width_indices = 1
        
        # ========== STEP 4: FIND PEAKS ==========
        try:
            peaks, properties = find_peaks(
                intensity_processed,
                prominence=prominence_threshold,
                distance=distance_indices,
                width=width_indices,
                height=height_threshold,
                rel_height=0.5
            )
        except:
            # Fallback to simpler peak finding
            peaks, properties = find_peaks(
                intensity_processed,
                prominence=prominence_threshold,
                distance=distance_indices
            )
        
        if len(peaks) == 0:
            return []
        
        # ========== STEP 5: CALCULATE RELATIVE INTENSITIES ==========
        max_intensity_processed = np.max(intensity_processed[peaks])
        if max_intensity_processed <= 0:
            return []
        
        # Connect to database if needed
        if match_with_db:
            self.connect_db()
        
        peak_list = []
        for i, peak_idx in enumerate(peaks):
            if peak_idx >= len(two_theta):
                continue
                
            two_theta_val = two_theta[peak_idx]
            intensity_raw_val = intensity[peak_idx]
            intensity_corrected_val = intensity_processed[peak_idx]
            
            # Relative intensity as percentage of STRONGEST peak
            intensity_percent = (intensity_corrected_val / max_intensity_processed) * 100.0
            
            # Only include peaks above configured relative intensity threshold
            if intensity_percent >= float(min_intensity_percent):
                # Calculate d-spacing using Bragg's Law
                d_spacing = self.converter.two_theta_to_d(two_theta_val)
                
                # Calculate FWHM if width data available
                fwhm = 0
                if 'widths' in properties and i < len(properties['widths']):
                    if len(two_theta) > 1:
                        step_size = two_theta[1] - two_theta[0]
                        fwhm = properties['widths'][i] * step_size
                
                # Create peak entry
                peak_entry = {
                    'index': int(peak_idx),
                    'two_theta': float(two_theta_val),
                    'd_spacing': float(d_spacing),
                    'intensity_raw': float(intensity_raw_val),
                    'intensity_corrected': float(intensity_corrected_val),
                    'intensity_percent': float(intensity_percent),
                    'prominence': float(properties['prominences'][i]) if i < len(properties['prominences']) else 0,
                    'fwhm': float(fwhm),
                    'noise_level': float(noise_std),
                    'name': None,
                    'formula': None,
                    'category': None,
                    'mineral_group': None,
                    'matches': []
                }
                
                # Match with database
                if match_with_db:
                    matches = self.match_peak_with_database(d_spacing, tolerance=0.02)
                    if matches:
                        peak_entry['matches'] = matches
                        peak_entry['name'] = matches[0]['name']
                        peak_entry['formula'] = matches[0]['formula']
                        peak_entry['category'] = matches[0]['category']
                        peak_entry['mineral_group'] = matches[0]['mineral_group']
                        peak_entry['best_match'] = matches[0]
                
                peak_list.append(peak_entry)
        
        # Close database connection
        if match_with_db:
            self.close_db()
        
        # ========== STEP 6: SORT BY INTENSITY ==========
        peak_list.sort(key=lambda x: x['intensity_percent'], reverse=True)
        
        # Add peak numbers
        for i, peak in enumerate(peak_list, 1):
            peak['peak_number'] = i
        
        return peak_list
    
    def format_peak_label(self, peak, format_type='short'):
        """
        Format peak information for display
        format_type: 'short', 'full', or 'list'
        """
        if format_type == 'short':
            if peak['name']:
                return f"{peak['two_theta']:.3f}° | {peak['d_spacing']:.4f}Å | {peak['intensity_percent']:.1f}% | {peak['name']}"
            else:
                return f"{peak['two_theta']:.3f}° | {peak['d_spacing']:.4f}Å | {peak['intensity_percent']:.1f}%"
        
        elif format_type == 'full':
            lines = []
            lines.append(f"Peak #{peak.get('peak_number', '?')}")
            lines.append(f"  2θ = {peak['two_theta']:.4f}°")
            lines.append(f"  d = {peak['d_spacing']:.4f} Å")
            lines.append(f"  I = {peak['intensity_percent']:.1f}%")
            if peak['name']:
                lines.append(f"  Mineral: {peak['name']}")
                if peak['formula']:
                    lines.append(f"  Formula: {peak['formula']}")
                if peak['mineral_group']:
                    lines.append(f"  Group: {peak['mineral_group']}")
                if 'best_match' in peak:
                    lines.append(f"  Match Δ = {peak['best_match']['delta']:.4f}Å")
            return "\n".join(lines)
        
        else:  # 'list' format for listbox
            if peak['name']:
                name_short = peak['name'][:15] if len(peak['name']) > 15 else peak['name']
                return f"{peak['peak_number']:2d}  {peak['two_theta']:7.3f}° {peak['d_spacing']:7.4f}Å {peak['intensity_percent']:5.1f}%  {name_short}"
            else:
                return f"{peak['peak_number']:2d}  {peak['two_theta']:7.3f}° {peak['d_spacing']:7.4f}Å {peak['intensity_percent']:5.1f}%"
    
    def get_peak_summary(self, peaks):
        """Generate a summary of detected peaks"""
        if not peaks:
            return "No peaks detected"
        
        summary = []
        summary.append(f"Total peaks: {len(peaks)}")
        
        # Count matched peaks
        matched = sum(1 for p in peaks if p['name'])
        summary.append(f"Matched in database: {matched}")
        
        # Strongest peak
        strongest = peaks[0]
        if strongest['name']:
            summary.append(f"Strongest: {strongest['name']} at {strongest['two_theta']:.3f}°")
        else:
            summary.append(f"Strongest peak at {strongest['two_theta']:.3f}°")
        
        return "\n".join(summary)
    
    def set_wavelength(self, wavelength):
        """Update wavelength and converter"""
        self.wavelength = wavelength
        self.converter = XRDConverter(wavelength=wavelength)


# ========== USAGE EXAMPLE ==========
if __name__ == "__main__":
    # Test the peak detector
    detector = PeakDetector()
    
    # Create sample data
    x = np.linspace(5, 90, 1000)
    y = 100 * np.exp(-(x-26.6)**2/0.5) + 30 * np.exp(-(x-50)**2/0.3) + np.random.normal(0, 2, 1000)
    
    # Detect peaks
    peaks = detector.detect_peaks(x, y, min_intensity_percent=5)
    
    print("\n" + "="*60)
    print("DETECTED PEAKS")
    print("="*60)
    
    for peak in peaks[:10]:  # Show first 10 peaks
        print(detector.format_peak_label(peak, format_type='list'))
    
    print("\n" + detector.get_peak_summary(peaks))