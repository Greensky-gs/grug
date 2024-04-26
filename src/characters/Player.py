from p5 import *
from utils.config import configs
from methods.parsers import parsePos

class Player:
    x = 0
    y = 0

    deltaV = 4
    deltaGrug = 7
    jumping: float = 0 # de 0 à 1 pour faire un coefficient
    shifting = False

    def __init__(self) -> None:
        pass

    def move(self, x, y):
        self.x, self.y = parsePos(self.x + x * self.deltaV, self.y + y * self.deltaV)

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