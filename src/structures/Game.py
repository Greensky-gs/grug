from characters import grug
from characters import Player
from utils.config import configs, renderModes, paths, dev
from methods.parsers import parseDirection, horizontal
from methods.paths import Pathing
from structures.Timer import Timer
from p5 import loadImage, image, fill, rect, resetMatrix, background
from os import listdir
from time import monotonic
from structures.BossManager import Bosses
from pprint import pprint

class Game:
    player: Player.Player
    grugSprite: grug.Grug
    mapIndex = 0
    bgIndex = None
    collisions = {
        "paths": Pathing(f"./src/data/paths.json", paths.Paths),
        "triggers": Pathing(f"./src/data/triggers.json", paths.Colliders)
    }
    ready = False
    paused = False
    tickerRef: int
    render = renderModes.UP
    bosses = Bosses()

    # Système de cache pour les arrières-plans
    bgCache = {}
    _cache = {}
    frameRate: int

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

        self.tickerRef = monotonic()
        self.bosses.load()
        self.ready = True

        if dev:
            self.setBgIndex("truck")
           
    def pause(self):
        self.paused = True
        self.cache("pauseTick", self.tick)
    def resume(self):
        self.paused = False
        self.cache("pauseTick")

    def setBgIndex(self, name):
        if name is None:
            self.cache("boss")
        
        boss = self.bosses.getBoss(name)
        if not boss:
            return
        
        self.cache("boss", boss)

        self.bgIndex = name
        self.collisions["ground"] = Pathing(f"./src/data/scenes/{name}.json", paths.Grounds)
        self.render = renderModes.FACE
        self.player.setTextureState("sprint")

        self.cache("beforeCollide", self.player.pos)
        self.player.moveTo(20, self.collisions["ground"].closest(self.player.x, self.player.y)[1])
    def resetBgIndex(self):
        self.bgIndex = None
        self.collisions.pop("ground")
        self.render = renderModes.UP
        self.player.setTextureState("idle")

        self.player.moveTo(*self.getcache("beforeCollide"))
        self.cache("beforeCollide")

    def cache(self, name, value = None):
        if value is None:
            if name in self._cache:
                self._cache.pop(name)
            return self._cache
        self._cache[name] = value
        return value
    def getcache(self, name, default = None):
        return self._cache.get(name, default)
    def startJump(self):
        self.player.setTextureState("jump")
        self.player.jumping = True
        self.cache("jumpTick", self.tick)

    def movePlayer(self, *, x = 0, y = 0, moving = False):
        if not self.player.jumping:
            if moving:
                self.player.setTextureState(self.playerMoveTexture)
                self.grugSprite.setTextureState("walk")
            else:
                self.player.setTextureState("idle")
                self.grugSprite.setTextureState("idle")

        if self.render == renderModes.FACE:
            y = 0
        self.player.move(x, y, paths=self.collisions["paths" if self.render == renderModes.UP else "ground"])
        
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

    def pauseScreen(self):
        self.grugSprite.display()
        self.player.display()

        fill(200, 200, 200, 200)
        rect(0, 0, configs["WIDTH"], configs["HEIGHT"])
    def display(self):
        self.player.tickTexture()

        resetMatrix()
        background(0)

        bg = self.bgCaching()
        image(bg, 0, 0)

        if self.paused:
            self.pauseScreen()
            return

        if self.render == renderModes.UP:
            self.grugSprite.display()
        if self.render == renderModes.FACE:
            boss = self.getcache("boss")
            if not not boss:
                boss.displayer()

            if self.player.jumping:
                self.player.addJump(self.getcache("jumpTick"), self.tick, self.collisions["ground"].closest(self.player.x, self.player.y)[1])
        self.player.display()

        self.checkTriggers()

    @property
    def tick(self):
        now = monotonic()
        return now - self.tickerRef
    
    @property
    def playerMoveTexture(self):
        return "walk" if self.render == renderModes.UP else "sprint"
