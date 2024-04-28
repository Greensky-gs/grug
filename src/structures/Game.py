from characters import grug
from characters import Player
from structures.Character import Character
from utils.config import configs
from methods.parsers import parseDirection, horizontal
from methods.paths import Pathing
from p5 import loadImage, image, text
from os import listdir

class Game:
    player: Player.Player
    grugSprite: grug.Grug
    mapIndex = 0
    bgIndex = None
    collisions = {
        "paths": Pathing(f"./src/data/paths.json", 0),
        "triggers": Pathing(f"./src/data/triggers.json", 1)
    }
    ready = False

    # Système de cache pour les arrières-plans
    bgCache = {}

    def __init__(self):
        pass
    
    def setup(self):
        self.player = Player.Player()
        self.grugSprite = grug.Grug(x = self.player.x, y = self.player.y)

        self.player.moveTo(40, 716)
        self.grugSprite.moveTo(*self.player.grugPos("right"))

        for file in listdir("./src/assets/bg"):
            name = file.split(".")[0]
            self.bgCache[name] = loadImage(f"./src/assets/bg/{name}.jpg")

        self.ready = True

    def setBgIndex(self, name):
        self.bgIndex = name
    def resetBgIndex(self):
        self.bgIndex = None

    def movePlayer(self, *, x = 0, y = 0, moving = False):
        if moving:
            self.player.setTextureState("walk")
            self.grugSprite.setTextureState("walk")
        else:
            self.player.setTextureState("idle")
            self.grugSprite.setTextureState("idle")

        self.player.tickTexture()

        self.player.move(x, y, paths=self.collisions["paths"])
        
        lastDir = parseDirection(x, y)

        if horizontal(lastDir):
            self.grugSprite.setLastX(lastDir)
        self.grugSprite.setLastDirection(lastDir)
        self.grugSprite.moveTo(*self.player.grugPos(self.grugSprite.lastDirection))

    def bgCaching(self):
        key = self.bgIndex if not self.bgIndex is None else self.mapIndex
        path = f"./src/assets/maps/{self.mapIndex}.jpg" if self.bgIndex is None else f"./src/assets/bg/{self.bgIndex}.jpg"

        if not key in self.bgCache:
            bg = loadImage(path)
            self.bgCache[key] = bg

            return bg
        return self.bgCache[key]
    def checkTriggers(self):
        if self.collisions["triggers"].inPath(self.player.x, self.player.y):
            scene = self.collisions["triggers"].getId(self.player.x, self.player.y)

            self.setBgIndex(scene)

    def display(self):
        bg = self.bgCaching()
        image(bg, 0, 0)

        self.grugSprite.display()
        self.player.display()

        self.checkTriggers()

