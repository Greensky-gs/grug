from p5 import *
from utils.config import renderModes, dev
from methods.parsers import parsePos, parseDirection, horizontal
from methods.paths import Pathing
from structures.Timer import Timer
from math import sin, pi, exp

class Player:
    x = 0
    y = 0

    deltaV = 4
    deltaSprint = 2 * deltaV
    deltaJump = 90
    deltaGrug = 45
    jumping: bool = False
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
        "sprint": {
            "counter": Timer(8),
            "textures": []
        },
        "jump": {
            "counter": Timer(1),
            "textures": []
        },
        "state": "idle"
    }
    lastDir = "right"

    def __init__(self) -> None:
        for i in range(8):
            walk = loadImage(f"./src/assets/sprites/player/walk/{i}.png")
            self.textures["walk"]["textures"].append(walk)

            sprint = loadImage(f"./src/assets/sprites/player/sprint/{i}.png")
            self.textures["sprint"]["textures"].append(sprint)

        self.textures["jump"]["textures"].append(loadImage("./src/assets/sprites/player/jump/0.png"))
        self.textures["idle"]["textures"].append(loadImage("./src/assets/sprites/player/idle/0.png"))
            
    def setTextureState(self, state):
        if state == self.textures["state"]:
            return

        self.textures[state]["counter"].reset()

        self.textures["state"] = state

    @property
    def delta(self):
        return self.deltaSprint if self.textures["state"] == "sprint" else self.deltaV
    def move(self, x, y, *, paths: Pathing):
        pos = parsePos(self.x + x * self.delta, self.y + y * self.delta)

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
    def addJump(self, startTick, currentTick, c):
        absis = (currentTick - startTick)
        
        # Amplitude du saut
        a = 0.4
        # Période du saut (longueur/durée)
        t = 1.3
        # Vitesse de décroissance
        l = -1.1

        jump = lambda x: (a * sin((pi * x)/t) * exp(-l * x))

        y = min(jump(absis) * self.deltaJump * -1, 0)

        if y >= 0 and startTick != currentTick:
            self.jumping = False
        self.y = y + c
    def tickTexture(self):
        self.textures[self.textures["state"]]["counter"].tick()


    def hitbox(self, w, h):
        fill(255)
        rect(self.x, self.y, w, h)
    def display(self):
        texture = self.textures[self.textures["state"]]
        img = texture["textures"][texture["counter"].count]

        if dev:
            self.hitbox(img.width, -img.height)
        pushMatrix()

        translate(self.x, self.y)

        coef = 0
        if self.lastDir == "left":
            scale(-1, 1)
            coef = -1
        image(img, img.width * coef, -img.height)

        popMatrix()

    def moveTo(self, x, y):
        self.x, self.y = parsePos(x, y)
