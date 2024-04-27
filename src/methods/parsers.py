from utils.config import configs
from typing import Literal

def parsePos(x, y):
    return (max(0, min(x, configs["WIDTH"] - 20)), max(0, min(y, configs["HEIGHT"] - 20)))
def parseDirection(x, y) -> Literal["up", "down", "left", "right"]:
    lastDir = None
    if x != 0:
        lastDir = "left" if x < 0 else "right"
    else:
        lastDir = "up" if y < 0 else "down"
    
    return lastDir