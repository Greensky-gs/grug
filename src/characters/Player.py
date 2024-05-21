from p5 import *
from utils.config import dev
from methods.parsers import parsePos, parseDirection, horizontal
from methods.paths import Pathing
from structures.Timer import Timer
from math import sin, pi, exp

class Player:
    x = 0
    y = 0

    deltaV = 4
    deltaSprint = 2 * deltaV
    deltaSpeedJump = 1.4 * deltaSprint
    deltaJump = 170
    deltaGrug = 45
    jumping: bool = False
    shifting = False
    dimens = [0, 0]

    hp = [50, 50]

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
    
    def reset(self):
        self.x = 0
        self.y = 0

        self.jumping = False
        self.shifting = False
        self.hp = [self.hp[1], self.hp[1]]
        self.lastDir = "right"

        self.textures["state"] = "idle"
        for key in self.textures:
            if key == "state":
                continue
            self.textures[key]["counter"].reset()

    def setTextureState(self, state):
        if state == self.textures["state"]:
            return

        self.textures[state]["counter"].reset()

        self.textures["state"] = state

    def hpBar(self):
        ox = 33
        oy = 789

        width = 270
        height = 10
        outline = 2

        noStroke()
        fill(0)
        rect(ox, oy, width + outline * 2, height + outline * 2)

        fill(125)
        rect(ox + outline, oy + outline, width, height)

        fill(6, 180, 59)
        rect(ox + outline, oy + outline, max(0, width * (self.hp[0] / self.hp[1])), height)
    @property
    def delta(self):
        return self.deltaSprint if self.textures["state"] == "sprint" else self.deltaSpeedJump if self.jumping else self.deltaV
    def move(self, x, y, *, paths: Pathing):
        pos = parsePos(self.x + x * self.delta, self.y + y * self.delta)

        if horizontal(parseDirection(x, y)):
            self.lastDir = parseDirection(x, y)

        if not paths.inPath(pos[0], pos[1]):
            pos = paths.closest(pos[0], pos[1])

            if abs(pos[0] - self.x) > 10 or abs(pos[1] - self.y) > 10:
                pos = parsePos(self.x, self.y)

        self.x, self.y = pos

    def resetPv(self):
        self.hp[0] = self.hp[1]
        return self
    @property
    def pos(self):
        return (self.x, self.y)
    
    def grugPos(self, direction):
        return [
            self.x + (self.deltaGrug if direction == "left" else -self.deltaGrug if direction == "right" else 0),
            self.y + (self.deltaGrug if direction == "up" else -self.deltaGrug if direction == "down" else 0)
        ]
    def addJump(self, startTick, currentTick, c, coefs = [0.7, 0.8, -1.1]):
        absis = (currentTick - startTick)

        a, t, l = coefs

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
    def damage(self, amount):
        self.hp[0] = max(self.hp[0] - amount, 0)
        return self.dead
    @property
    def dead(self):
        return self.hp[0] <= 0
    def display(self):
        texture = self.textures[self.textures["state"]]
        img = texture["textures"][texture["counter"].count]

        self.dimens = [img.width, img.height]

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
    @property
    def width(self):
        return self.dimens[0]
    @property
    def height(self):
        return self.dimens[1]
