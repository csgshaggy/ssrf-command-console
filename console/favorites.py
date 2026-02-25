"""
favorites.py
Simple favorites manager for the SSRF Command Console.
"""

import json
import os

class Favorites:
    def __init__(self, file="favorites.json"):
        self.file = file
        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump([], f)

    def all(self):
        with open(self.file, "r") as f:
            return json.load(f)

    def add(self, mode: str):
        favs = self.all()
        if mode not in favs:
            favs.append(mode)
        with open(self.file, "w") as f:
            json.dump(favs, f, indent=2)

    def remove(self, mode: str):
        favs = self.all()
        if mode in favs:
            favs.remove(mode)
        with open(self.file, "w") as f:
            json.dump(favs, f, indent=2)
