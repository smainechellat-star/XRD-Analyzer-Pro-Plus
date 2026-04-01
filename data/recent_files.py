"""Recent files history management."""

import json
import os
from datetime import datetime


class RecentFiles:
    def __init__(self, storage_path, max_items=10):
        self.storage_path = storage_path
        self.max_items = max_items
        self._items = []
        self.load()

    def load(self):
        if not os.path.exists(self.storage_path):
            self._items = []
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                self._items = json.load(f)
        except Exception:
            self._items = []

    def save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self._items, f, indent=2)

    def add(self, filepath):
        self._items = [item for item in self._items if item.get("path") != filepath]
        self._items.insert(0, {"path": filepath, "opened_at": datetime.now().isoformat()})
        self._items = self._items[: self.max_items]
        self.save()

    def list(self):
        return list(self._items)
