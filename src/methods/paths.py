from json import load
from typing import Dict, List
from utils.config import paths

class Pathing:
    paths: Dict[str, List[int]] = {}
    mode: int

    def __init__(self, path, mode):
        self.paths = load(open(path, "r"))
        self.mode = mode
    
    def inPath(self, x, y):
        if self.mode == paths.Paths or self.mode == paths.Colliders:
            if not str(x) in self.paths:
                return False
            return y in self.paths[str(x)] or str(y) in self.paths[str(x)]
        if self.mode == paths.Grounds:
            return y <= self.paths["ground"]
    def closest(self, x, y):
        if self.mode == paths.Paths:
            closestX = min(self.paths.keys(), key=lambda k: abs(int(k) - x))
            closestY = min(self.paths[closestX], key=lambda k: abs(int(k) - y))

            return (int(closestX), int(closestY))
        if self.mode == paths.Grounds:
            return (x, self.paths["ground"])
    def getId(self, x, y):
        if self.mode != paths.Colliders:
            raise AttributeError("Les ids ne sont disponibles que dans le mode 'Collider'")
        if not self.inPath(x, y):
            return None
        
        return self.paths[str(x)][str(y)]
    