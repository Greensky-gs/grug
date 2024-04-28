from p5 import *
from utils.config import configs
from methods.parsers import parsePos, parseDirection, horizontal
from methods.paths import Pathing
from structures.Timer import Timer

class Player:
    x = 0
    y = 0

    deltaV = 4
    deltaGrug = 30
    jumping: float = 0 # de 0 à 1 pour faire un coefficient
    shifting = False

    textures = {
        "walk": {
            "counter": Timer(8),
            "textures": []
        },
        "idle": {
            "counter": Timer(1),
            "textures": []
        },
        "state": "idle"
    }
    lastDir = "right"

    def __init__(self) -> None:
        for i in range(8):
            img = loadImage(f"./src/assets/sprites/player/walk/{i}.png")
            self.textures["walk"]["textures"].append(img)
        self.textures["idle"]["textures"].append(loadImage("./src/assets/sprites/player/idle/0.png"))
            
    def setTextureState(self, state):
        if state == self.textures["state"]:
            return

        self.textures[state]["counter"].reset()

        self.textures["state"] = state

    def move(self, x, y, *, paths: Pathing):
        pos = parsePos(self.x + x * self.deltaV, self.y + y * self.deltaV)

        if horizontal(parseDirection(x, y)):
            self.lastDir = parseDirection(x, y)

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
    def tickTexture(self):
        self.textures[self.textures["state"]]["counter"].tick()

    def display(self):
        texture = self.textures[self.textures["state"]]

        pushMatrix()

        height = 60
        width = 20

        translate(self.x, self.y)

        if self.lastDir == "left":
            scale(-1, 1)

        image(texture["textures"][texture["counter"].count], -width, -height)

        popMatrix()

    def moveTo(self, x, y):
        self.x, self.y = parsePos(x, y)