from json import load
from typing import Dict, List

class Pathing:
    paths: Dict[str, List[int]] = {}
    mode: int

    def __init__(self, path, mode):
        self.paths = load(open(path, "r"))
        self.mode = mode
    
    def inPath(self, x, y):
        if self.mode == 0 or self.mode == 1:
            if not str(x) in self.paths:
                return False
            return y in self.paths[str(x)] or str(y) in self.paths[str(x)]
    def closest(self, x, y):
        if self.mode == 0:
            closestX = min(self.paths.keys(), key=lambda k: abs(int(k) - x))
            closestY = min(self.paths[closestX], key=lambda k: abs(int(k) - y))

            return (int(closestX), int(closestY))
    def getId(self, x, y):
        if self.mode != 1:
            raise AttributeError("Les ids ne sont disponibles que dans le mode 1")
        if not self.inPath(x, y):
            return None
        
        return self.paths[str(x)][str(y)]
    