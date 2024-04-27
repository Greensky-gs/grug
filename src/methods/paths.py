from json import load
from typing import Dict, List

class Pathing:
    paths: Dict[str, List[int]] = {}

    def __init__(self):
        self.paths = load(open("src/data/paths.json"))
    
    def inPath(self, x, y):
        if not str(x) in self.paths:
            return False
        return y in self.paths[str(x)]
    def closest(self, x, y):
        closestX = min(self.paths.keys(), key=lambda k: abs(int(k) - x))
        closestY = min(self.paths[closestX], key=lambda k: abs(int(k) - y))

        return (int(closestX), int(closestY))
    