"""
XRD CONVERTER - Fixed version that NEVER returns zeros
"""

import numpy as np
import os

def convert_to_ascii(xrd_data):
    """
    Convert any XRD data to ASCII with SAFE intensity handling
    """
    if xrd_data is None:
        raise ValueError("No data to convert")
    
    # ===== SAFELY GET INTENSITY DATA =====
    intensity = None
    
    # Try multiple possible keys for intensity
    for key in ['intensity_raw', 'intensity', 'counts', 'data', 'y']:
        if key in xrd_data:
            intensity = np.array(xrd_data[key])
            print(f"✅ Found intensity using key: '{key}'")
            break
    
    if intensity is None:
        raise ValueError("No intensity data found in file")
    
    # Remove invalid values
    original_len = len(intensity)
    intensity = intensity[~np.isnan(intensity)]
    intensity = intensity[~np.isinf(intensity)]
    
    print(f"📊 Intensity points: {original_len} → {len(intensity)} after cleaning")
    
    if len(intensity) == 0:
        raise ValueError("No valid intensity data after cleaning")
    
    # ===== CHECK FOR ZERO INTENSITY =====
    max_int = np.max(intensity)
    if max_int == 0:
        print("⚠️ WARNING: Max intensity is ZERO!")
        # Try to recover - maybe it's all zeros?
        if np.all(intensity == 0):
            raise ValueError("All intensity values are zero - file may be corrupted")
    
    print(f"📈 Intensity range: {np.min(intensity):.0f} - {max_int:.0f}")
    
    # ===== FORCE 2θ RANGE =====
    n_points = len(intensity)
    two_theta = np.linspace(5.0, 150.0, n_points)
    
    print(f"✅ Using forced 2θ range: 5.0° - 150.0° ({n_points} points)")
    
    # Create ASCII data structure
    ascii_data = {
        'two_theta': two_theta,
        'intensity_raw': intensity,
        'format': 'ASCII (converted)',
        'original_format': xrd_data.get('format', 'Unknown'),
        'points': n_points,
        'range': "5.0-150.0°",
        'intensity_max': float(max_int),
        'intensity_min': float(np.min(intensity))
    }
    
    return ascii_data

def save_as_ascii(xrd_data, output_path):
    """
    Save XRD data as 2-column ASCII file
    """
    ascii_data = convert_to_ascii(xrd_data)
    
    # Create safe header
    header = f"# Converted from {xrd_data.get('format', 'Unknown')}\n"
    header += f"# Original file: {xrd_data.get('filename', 'unknown')}\n"
    header += f"# 2θ range: 5.0° - 150.0° (forced)\n"
    header += f"# Intensity range: {ascii_data['intensity_min']:.0f} - {ascii_data['intensity_max']:.0f}\n"
    header += "# 2theta(deg)  Intensity(counts)"
    
    # Save with UTF-8 encoding
    np.savetxt(output_path, 
              np.column_stack((ascii_data['two_theta'], ascii_data['intensity_raw'])),
              fmt='%.4f %.2f',
              header=header,
              comments='',
              encoding='utf-8')
    
    print(f"✅ Saved ASCII: {output_path}")
    print(f"   2θ range: 5.0° - 150.0°")
    print(f"   Intensity range: {ascii_data['intensity_min']:.0f} - {ascii_data['intensity_max']:.0f}")
    
    return output_path
