from utils.config import configs
from typing import Literal
from random import randint

DirectionType = Literal["up", "down", "left", "right"]

def parsePos(x, y, *, aw = 0):
    # Fonction pour analyser et limiter les coordonnées de position
    return (max(0, min(x, configs["WIDTH"] - (20 + aw))), max(0, min(y, configs["HEIGHT"] - 20)))

def parseDirection(x, y) -> DirectionType:
    # Fonction pour analyser la direction en fonction des coordonnées x et y
    lastDir = None
    if x != 0:
        lastDir = "left" if x < 0 else "right"
    else:
        lastDir = "up" if y < 0 else "down"
    
    return lastDir

def horizontal(direction: DirectionType) -> bool:
    # Fonction pour vérifier si la direction est horizontale
    return direction in ["left", "right"]

def vertical(direction: DirectionType) -> bool:
    # Fonction pour vérifier si la direction est verticale
    return direction in ["up", "down"]

def oppositeDirection(direction: DirectionType) -> DirectionType:
    # Fonction pour obtenir la direction opposée
    return "left" if direction == "right" else "right" if direction == "left" else "up" if direction == "down" else "down"

def randomDirection(excludedDirections: list[DirectionType] = []):
    # Fonction pour obtenir une direction aléatoire, en excluant les directions spécifiées
    directions = list(filter(lambda x: not x in excludedDirections, ["up", "down", "left", "right"]))
    return directions[randint(0, len(directions) - 1)]

def checkCollision(*, oxa, oya, oxb, oyb, wa, ha, wb, hb):
    # Fonction pour vérifier la collision entre deux objets
    return oxa < oxb + wb and oya < oyb + hb and oxb < oxa + wa and oyb < oya + ha