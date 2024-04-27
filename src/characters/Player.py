from p5 import *
from utils.config import configs
from methods.parsers import parsePos
from methods.paths import Pathing

class Player:
    x = 0
    y = 0

    deltaV = 4
    deltaGrug = 7
    jumping: float = 0 # de 0 à 1 pour faire un coefficient
    shifting = False

    def __init__(self) -> None:
        pass

    def move(self, x, y, paths: Pathing):
        pos = parsePos(self.x + x * self.deltaV, self.y + y * self.deltaV)
        if not paths.inPath(pos[0], pos[1]):
            pos = paths.closest(pos[0], pos[1])

            if abs(pos[0] - self.x) > 10 or abs(pos[1] - self.y) > 10:
                pos = parsePos(self.x, self.y)

        self.x, self.y = pos

    @property
    def pos(self):
        return (self.x, self.y)
    
    def grugPos(self, direction):
        return [
            self.x + (self.deltaGrug if direction == "left" else -self.deltaGrug if direction == "right" else 0),
            self.y + (self.deltaGrug if direction == "up" else -self.deltaGrug if direction == "down" else 0)
        ]

    def display(self):
        fill(255)
        rect(self.x, self.y, 10, 10)
    def moveTo(self, x, y):
        self.x, self.y = parsePos(x, y)