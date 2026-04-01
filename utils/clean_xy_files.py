"""
Utility to clean and normalize .xy files for XRD analysis
Removes comments, headers, tabs, and ensures proper format
"""

import sys


def clean_xy(input_path, output_path):
    """
    Clean and normalize .xy file format
    
    Args:
        input_path: Path to input .xy file
        output_path: Path to output cleaned .xy file
    """
    with open(input_path, 'r', encoding='utf-8') as f_in:
        lines = f_in.readlines()
    
    cleaned = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines, comments, and headers
        if not line or line.startswith('#') or line.startswith('2theta') or line.startswith('2Theta'):
            continue
        
        # Handle tabs and split
        parts = line.replace('\t', ' ').split()
        
        # Extract first two numeric columns
        if len(parts) >= 2:
            try:
                two_theta = float(parts[0])
                intensity = float(parts[1])
                cleaned.append(f"{parts[0]} {parts[1]}")
            except ValueError:
                # Skip lines that don't have valid numeric values
                continue
    
    # Write cleaned file
    with open(output_path, 'w', encoding='utf-8') as f_out:
        f_out.write("\n".join(cleaned))
    
    print(f"✓ Cleaned file saved to: {output_path}")
    print(f"  Lines processed: {len(cleaned)}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python clean_xy_files.py <input_file> <output_file>")
        print("Example: python clean_xy_files.py raw.xy cleaned.xy")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        clean_xy(input_file, output_file)
        print("✓ Normalization complete!")
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
