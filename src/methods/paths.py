from json import load
from typing import Dict, List
from utils.config import paths
from pprint import pprint

class Pathing:
    paths: Dict[str, List[int]] = {}  # Dictionnaire contenant les chemins avec leurs coordonnées
    mode: int  # Mode de fonctionnement du Pathing

    def __init__(self, path, mode):
        self.paths = load(open(path, "r"))  # Charger les chemins à partir du fichier JSON
        self.mode = mode
    
    def inPath(self, x, y):
        if self.mode == paths.Paths or self.mode == paths.Colliders:
            if not str(x) in self.paths:  # Vérifier si la coordonnée x existe dans les chemins
                return False
            return y in self.paths[str(x)] or str(y) in self.paths[str(x)]  # Vérifier si la coordonnée y existe dans les chemins
        if self.mode == paths.Grounds:
            return y <= self.paths["ground"]  # Vérifier si la coordonnée y est inférieure ou égale à la coordonnée "ground"
    
    def closest(self, x, y):
        if self.mode == paths.Paths:
            closestX = min(self.paths.keys(), key=lambda k: abs(int(k) - x))  # Trouver la coordonnée x la plus proche de x
            closestY = min(self.paths[closestX], key=lambda k: abs(int(k) - y))  # Trouver la coordonnée y la plus proche de y

            return (int(closestX), int(closestY))  # Retourner les coordonnées les plus proches
        if self.mode == paths.Grounds:
            return (x, self.paths["ground"])  # Retourner les coordonnées x et "ground"
    
    def getId(self, x, y):
        if self.mode != paths.Colliders:
            raise AttributeError("Les ids ne sont disponibles que dans le mode 'Collider'")  # Lever une exception si le mode n'est pas "Collider"
        if not self.inPath(x, y):
            return None
        
        return self.paths[str(x)][str(y)]  # Retourner l'ID correspondant aux coordonnées x et y
    
    def removeKey(self, key):
        if self.mode != paths.Colliders:
            raise AttributeError("Il n'est possible de supprimer des clés que dans le mode 'Collider'")  # Lever une exception si le mode n'est pas "Collider"
        
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
                    del self.paths[x][y]  # Supprimer la clé correspondant à la valeur donnée
    