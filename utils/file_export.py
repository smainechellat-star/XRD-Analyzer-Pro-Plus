"""
CSV EXPORT MODULE - With ±0.02° tolerance
"""

import csv
import os
import numpy as np
from datetime import datetime

class PeakExporter:
    """Export detected peaks to CSV with tolerance information"""
    
    @staticmethod
    def export_peaks(peaks, original_filename=None, output_path=None, 
                    processing_params=None, tolerance=0.02):
        """
        Export peaks to CSV with ±0.02° tolerance information
        
        Args:
            peaks: List of peak dictionaries
            original_filename: Source XRD file name
            output_path: Custom output path
            processing_params: Processing parameters used
            tolerance: Tolerance in degrees (default: 0.02)
        """
        if not peaks:
            raise ValueError("No peaks to export")
        
        # Filter peaks by intensity >5%
        peaks = [p for p in peaks if p.get('intensity_percent', 0) >= 5.0]
        
        if not peaks:
            raise ValueError("No peaks with intensity >5% found")
        
        # Generate filename
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if original_filename:
                base = os.path.splitext(os.path.basename(original_filename))[0]
                filename = f"{base}_peaks_{timestamp}.csv"
            else:
                filename = f"xrd_peaks_{timestamp}.csv"
            output_path = os.path.join(os.getcwd(), filename)
        
        # Ensure .csv extension
        if not output_path.endswith('.csv'):
            output_path += '.csv'
        
        # Create directory if needed
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # === HEADER WITH TOLERANCE INFORMATION ===
            writer.writerow(['#', '=' * 80])
            writer.writerow(['# XRD PEAK ANALYSIS REPORT'])
            writer.writerow(['#', '=' * 80])
            writer.writerow(['# Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            
            if original_filename:
                writer.writerow(['# Source File:', os.path.basename(original_filename)])
            
            writer.writerow(['# Total Peaks (>5%):', len(peaks)])
            writer.writerow(['# Intensity Threshold:', '>5% of maximum'])
            writer.writerow(['# Peak Position Tolerance:', f'±{tolerance}° 2θ (Hanawalt method)'])
            writer.writerow(['# Wavelength:', '1.5406 Å (Cu Kα)'])
            writer.writerow(['#'])
            
            # Processing parameters
            if processing_params:
                writer.writerow(['# PROCESSING PARAMETERS'])
                for key, value in processing_params.items():
                    writer.writerow([f'# {key}:', value])
                writer.writerow(['#'])
            
            writer.writerow(['# PEAK LIST (sorted by intensity)'])
            writer.writerow(['# Position uncertainty: ±0.02° 2θ (±0.015-0.030 Å d-spacing)'])
            writer.writerow(['#'])
            
            # === COLUMN HEADERS ===
            writer.writerow([
                'Peak_No',
                '2θ (deg)',
                '±Tolerance (deg)',
                'd-spacing (Å)',
                '±Tolerance (Å)',
                'Intensity (counts)',
                'Intensity (%)',
                'FWHM (deg)',
                'Peak_Prominence',
                'Peak_Width (2θ)'
            ])
            
            # === DATA ROWS ===
            for i, peak in enumerate(sorted(peaks, 
                                          key=lambda x: x['intensity_percent'], 
                                          reverse=True), 1):
                
                # Calculate d-spacing tolerance (angle-dependent)
                two_theta = peak.get('two_theta', 0)
                d_spacing = peak.get('d_spacing', 0)
                
                # d-spacing tolerance varies with angle
                # Using derivative of Bragg's law: Δd/d = -cot(θ) Δθ
                theta = two_theta / 2
                theta_rad = np.radians(theta)
                cot_theta = 1 / np.tan(theta_rad) if np.tan(theta_rad) != 0 else 0
                d_tolerance = abs(d_spacing * cot_theta * np.radians(tolerance))
                
                writer.writerow([
                    i,
                    f"{two_theta:.4f}",
                    f"±{tolerance:.3f}",
                    f"{d_spacing:.4f}",
                    f"±{d_tolerance:.4f}",
                    f"{peak.get('intensity_raw', 0):.0f}",
                    f"{peak.get('intensity_percent', 0):.2f}",
                    f"{peak.get('fwhm', 0):.4f}",
                    f"{peak.get('prominence', 0):.2f}",
                    f"{peak.get('width', 0):.4f}"
                ])
            
            # === SUMMARY STATISTICS ===
            writer.writerow([])
            writer.writerow(['#', '-' * 60])
            writer.writerow(['# TOLERANCE INFORMATION'])
            writer.writerow(['#', '-' * 60])
            writer.writerow(['# The ±0.02° 2θ tolerance accounts for:'])
            writer.writerow(['# • Instrumental reproducibility (diffractometer precision)'])
            writer.writerow(['# • Sample displacement errors'])
            writer.writerow(['# • Natural mineral variability (solid solution, microstrain)'])
            writer.writerow(['# • Calibration drift'])
            writer.writerow(['#'])
            writer.writerow(['# This follows the Hanawalt method (1938) and modern'])
            writer.writerow(['# practices in HighScore Plus for phase identification.'])
        
        return os.path.abspath(output_path)
