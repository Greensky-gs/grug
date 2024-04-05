from p5 import *
from utils.config import configs

class Player:
    x = 0
    y = 0

    deltaV = 100
    jumping: float = 0 # de 0 à 1 pour faire un coefficient
    shifting = False

    def __init__(self) -> None:
        pass

    def move(self, *, x = 0, y = 0):
        self.x = max(0, min(configs["WIDTH"], self.x + x * self.deltaV))
        self.y += y * self.deltaV

    def display(self):
        print(self.x, self.y)
        rect(self.x, self.y, 10, 10)