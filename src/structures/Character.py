from p5 import *
from methods.parsers import parsePos
class Character:
    drawer = None  # Le dessinateur pour afficher le personnage
    pos = [0, 0]  # La position du personnage
    name = None  # Le nom du personnage

    def __init__(self, *, x, y, name) -> None:
        self.name = name
        self.pos = [x, y]
    
    def setDrawer(self, drawer):
        self.drawer = drawer

    def setPos(self, x, y):
        self.pos = list(parsePos(x, y))  # Convertir les coordonnées en une liste
    def display(self):
        fill(0)  # Remplir la forme avec la couleur noire
        self.drawer(*self.pos)  # Appeler la fonction de dessin avec les coordonnées du personnage
