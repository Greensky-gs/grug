from p5 import *
from methods.parsers import parsePos

class Character:
    drawer = None
    pos = [0, 0]
    name = None

    def __init__(self, *, x, y, name) -> None:
        self.name = name
        self.pos = [x, y]
    
    def setDrawer(self, drawer):
        self.drawer = drawer

    def setPos(self, x, y):
        self.pos = list(parsePos(x, y))
    def display(self):
        fill(0)
        self.drawer(*self.pos)