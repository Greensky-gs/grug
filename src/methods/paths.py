from json import load
from typing import Dict, List
from utils.config import paths
from pprint import pprint

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
    def removeKey(self, key):
        if self.mode != paths.Colliders:
            raise AttributeError("Il n'est possible de supprimer des clés que dans le mode 'Collider'")
        
        pprint(self.paths)    
        xList = list(self.paths.keys())
        for x in xList:
            if not x in self.paths:
                continue
            yList = list(self.paths[x].keys())

            for y in yList:
                if not y in self.paths[x]:
                    continue
                print(self.paths[x][y])
                if self.paths[x][y] == key:
                    del self.paths[x][y]
        pprint(self.paths)
    