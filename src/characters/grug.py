from structures.Character import Character
from p5 import *
from typing import Literal
from structures.Timer import Timer
from pprint import pprint
from utils.config import dev

class Grug:
    name = "Grug"
    pos = [0, 0]
    pnj: Character
    lastDir: Literal["up", "down", "left", "right"] = None
    lastX: Literal["left", "right"] = "right"

    textures = {
        "walk": {
            "timer": Timer(23),
            "textures": []
        },
        "idle": {
            "timer": Timer(17),
            "textures": []
        },
        "state": "idle",
        "ticker": Timer(3)
    }

    def __init__(self, *, x, y) -> None:
        self.pos = [x, y]
        self.pnj = Character(x = self.pos[0], y = self.pos[1], name = self.name)

        # Chargement des textures
        for i in range(1, 24):
            txtI = str(i).zfill(3)

            self.textures["walk"]["textures"].append(loadImage(f"./src/assets/sprites/grug/walk/0_Ogre_Walking_{txtI}.png"))
            if i <= 17:
                self.textures["idle"]["textures"].append(loadImage(f"./src/assets/sprites/grug/idle/0_Ogre_Idle_{txtI}.png"))

        # La fonction d'affichage de grug
        def drawer(x, y):
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

            popMatrix()
        self.pnj.setDrawer(drawer)

    def setLastX(self, lastX):
        self.lastX = lastX
    def display(self):
        self.pnj.display()

    def setTextureState(self, state):
        if self.textures["state"] == state:
            return
    
        self.textures[self.textures["state"]]["timer"].reset()
        self.textures["state"] = state

    def moveTo(self, x, y):
        self.pnj.setPos(x, y)
    
    def setLastDirection(self, direction):
        self.lastDir = direction
    @property
    def lastDirection(self):
        return self.lastDir if not self.lastDir is None else "down"