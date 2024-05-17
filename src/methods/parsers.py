from utils.config import configs
from typing import Literal

def parsePos(x, y, *, aw = 0):
    return (max(0, min(x, configs["WIDTH"] - (20 + aw))), max(0, min(y, configs["HEIGHT"] - 20)))
def parseDirection(x, y) -> Literal["up", "down", "left", "right"]:
    lastDir = None
    if x != 0:
        lastDir = "left" if x < 0 else "right"
    else:
        lastDir = "up" if y < 0 else "down"
    
    return lastDir
def horizontal(dir):
    return dir in ["left", "right"]
def vertical(dir):
    return dir in ["up", "down"]