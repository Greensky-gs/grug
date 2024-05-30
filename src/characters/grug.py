from structures.Character import Character
from p5 import *
from typing import Literal
from structures.Timer import Timer
from pprint import pprint
from utils.config import dev

class Grug:
    # Classe représentant le personnage Grug

    name = "Grug"  # Nom du personnage
    pos = [0, 0]  # Position du personnage
    pnj: Character  # Personnage non-joueur
    lastDir: Literal["up", "down", "left", "right"] = None  # Dernière direction du personnage
    lastX: Literal["left", "right"] = "right"  # Dernière direction horizontale du personnage

    textures = {
        "walk": {  # Textures pour la marche
            "timer": Timer(23),  # Timer pour l'animation de la marche
            "textures": []  # Textures de la marche
        },
        "idle": {  # Textures pour l'immobilité
            "timer": Timer(17),  # Timer pour l'animation de l'immobilité
            "textures": []  # Textures de l'immobilité
        },
        "hat": None,  # Texture du chapeau
        "state": "idle",  # État actuel du personnage
        "ticker": Timer(3)  # Timer pour le changement d'état
    }

    def __init__(self, *, x, y) -> None:
        # Initialisation du personnage Grug avec une position donnée

        self.pos = [x, y]  # Définition de la position
        self.pnj = Character(x=self.pos[0], y=self.pos[1], name=self.name)  # Création du personnage non-joueur

        # Chargement des textures
        for i in range(1, 24):
            txtI = str(i).zfill(3)

            self.textures["hat"] = loadImage("./src/assets/hats/haut_forme.png")
            self.textures["walk"]["textures"].append(loadImage(f"./src/assets/sprites/grug/walk/0_Ogre_Walking_{txtI}.png"))
            if i <= 17:
                self.textures["idle"]["textures"].append(loadImage(f"./src/assets/sprites/grug/idle/0_Ogre_Idle_{txtI}.png"))

        # La fonction d'affichage de grug
        def drawer(x, y):
            # Fonction pour afficher le personnage Grug

            texture = self.textures[self.textures["state"]]

            self.textures["ticker"].tick()
            if self.textures["state"] == "idle":
                if self.textures["ticker"].valid:
                    texture["timer"].tick()
            else:
                texture["timer"].tick()

            img = texture["textures"][texture["timer"].count]

            if dev:
                print("dev")
                fill(255)
                rect(self.pos[0], self.pos[1], img.width, -img.height)

            pushMatrix()

            translate(x, y)

            coef = 0
            if self.lastX == "left":
                coef = -1
                scale(-1, 1)

            image(img, coef * img.width, -img.height)
            hat = self.textures["hat"]
            image(hat, coef * hat.width, -img.height - hat.height / 2.5)

            popMatrix()

        self.pnj.setDrawer(drawer)  # Définition de la fonction d'affichage du personnage non-joueur

    def setLastX(self, lastX):
        # Définit la dernière direction horizontale du personnage

        self.lastX = lastX

    def display(self):
        # Affiche le personnage

        self.pnj.display()

    def setTextureState(self, state):
        # Définit l'état des textures du personnage

        if self.textures["state"] == state:
            return

        self.textures[self.textures["state"]]["timer"].reset()
        self.textures["state"] = state

    def moveTo(self, x, y):
        # Déplace le personnage à une position donnée

        self.pnj.setPos(x, y)

    def setLastDirection(self, direction):
        # Définit la dernière direction du personnage

        self.lastDir = direction

    @property
    def lastDirection(self):
        # Renvoie la dernière direction du personnage

        return self.lastDir if not self.lastDir is None else "down"