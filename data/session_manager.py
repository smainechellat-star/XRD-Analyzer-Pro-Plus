"""Save/load lightweight session metadata."""

import json
import os
from datetime import datetime


class SessionManager:
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def save(self, current_data=None):
        payload = {
            "saved_at": datetime.now().isoformat(),
            "current": self._extract_metadata(current_data),
        }
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def load(self):
        if not os.path.exists(self.storage_path):
            return None
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def _extract_metadata(self, data):
        if not data:
            return None
        return {
            "filename": data.get("filename"),
            "format": data.get("format"),
            "points": len(data.get("two_theta", [])),
        }
