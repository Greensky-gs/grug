from structures.Character import Character
from p5 import *
from typing import Literal

class Grug:
    name = "Grug"
    pos = [0, 0]
    pnj: Character
    lastDir: Literal["up", "down", "left", "right"] = None

    def __init__(self, *, x, y) -> None:
        self.pos = [x, y]
        self.pnj = Character(x = self.pos[0], y = self.pos[1], name = self.name)

        # La fonction d'affichage de grug
        def drawer(x, y):
            fill(255, 0, 0)
            rect(x, y, 10, 10)
        self.pnj.setDrawer(drawer)

    def display(self):
        self.pnj.display()

    def moveTo(self, x, y):
        self.pnj.setPos(x, y)
    
    def setLastDirection(self, direction):
        self.lastDir = direction
    @property
    def lastDirection(self):
        return self.lastDir if not self.lastDir is None else "down"
