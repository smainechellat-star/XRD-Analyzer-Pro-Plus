"""Central data state manager."""

import os
from datetime import datetime

import numpy as np

from data.recent_files import RecentFiles
from data.session_manager import SessionManager


class DataManager:
    def __init__(self):
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        self.current_data = None
        self.processing_params = None  # NEW: Store processing parameters from Home screen
        self.recent_files = RecentFiles(os.path.join(data_dir, "recent_files.json"))
        self.session_manager = SessionManager(os.path.join(data_dir, "session.json"))
        self.last_session = self.session_manager.load()

    def add_recent_file(self, filepath):
        self.recent_files.add(filepath)

    def save_session(self):
        self.session_manager.save(self.current_data)

    def load_file(self, filepath):
        """Load XRD file and FORCE 2θ range to 5°-150°"""
        from processing.file_parsers import UniversalXRDReader

        try:
            reader = UniversalXRDReader()
            data = reader.parse_file(filepath)

            # Critical safety checks
            if "intensity_raw" not in data:
                return False, "Invalid data format: missing intensity data"

            if len(data["intensity_raw"]) == 0:
                return False, "No intensity data points extracted from file"

            if len(data["intensity_raw"]) < 5:
                return False, f"Insufficient data points: {len(data['intensity_raw'])} (minimum 5)"
            
            # ===== FORCE 2θ RANGE TO 5°-150° =====
            n_points = len(data["intensity_raw"])
            data["two_theta"] = np.linspace(5.0, 150.0, n_points)
            print(f"✅ Forced 2θ range: 5.0° - 150.0° ({n_points} points)")

            # Normalize with safety check
            max_int = np.max(data["intensity_raw"])
            if max_int > 0 and not np.isnan(max_int) and not np.isinf(max_int):
                data["intensity_normalized"] = (data["intensity_raw"] / max_int) * 100.0
            else:
                data["intensity_normalized"] = data["intensity_raw"] * 100.0
                print(f"Warning: max intensity was {max_int}, using fallback normalization")

            data["filename"] = os.path.basename(filepath)
            data["filepath"] = filepath
            data["load_time"] = datetime.now().isoformat()
            data["forced_range"] = "5°-150°"

            self.current_data = data
            self.add_recent_file(filepath)

            return True, f"Loaded {data.get('format', 'Unknown')} with {n_points} points (forced 5°-150° range)"

        except Exception as exc:
            return False, str(exc)

    def load_converted_data(self, ascii_data):
        """
        Load converted ASCII data into the app
        This is the ONLY format the app uses internally after conversion
        
        Args:
            ascii_data: Dictionary with 'two_theta' and 'intensity_raw'
        
        Returns:
            Boolean success status
        """
        # Normalize intensity
        if 'intensity_raw' in ascii_data:
            max_int = np.max(ascii_data['intensity_raw'])
            if max_int > 0 and not np.isnan(max_int) and not np.isinf(max_int):
                ascii_data['intensity_normalized'] = (ascii_data['intensity_raw'] / max_int) * 100.0
            else:
                ascii_data['intensity_normalized'] = ascii_data['intensity_raw'] * 100.0
        
        # Add metadata
        ascii_data['load_time'] = datetime.now().isoformat()
        ascii_data['format'] = 'ASCII (converted)'
        
        self.current_data = ascii_data
        return True
