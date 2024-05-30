from characters import grug
from characters import Player
from utils.config import configs, renderModes, paths, dev
from methods.parsers import parseDirection, horizontal, checkCollision
from methods.paths import Pathing
from structures.Timer import Timer
from p5 import loadImage, image, fill, rect, resetMatrix, background
from os import listdir
from time import monotonic
from structures.BossManager import Bosses
from pprint import pprint

class Game:
    player: Player.Player  # Instance of the Player class
    grugSprite: grug.Grug  # Instance of the grug.Grug class
    mapIndex = 0  # Index of the current map
    bgIndex = None  # Index of the current background
    collisions = {
        "paths": Pathing(f"./src/data/paths.json", paths.Paths),  # Collision paths
        "triggers": Pathing(f"./src/data/triggers.json", paths.Colliders)  # Collision triggers
    }
    ready = False  # Flag indicating if the game is ready to be played
    paused = False  # Flag indicating if the game is paused
    loading = True  # Flag indicating if the game is currently loading
    tickerRef: int  # Reference time for calculating tick
    render = renderModes.UP  # Rendering mode
    bosses = Bosses()  # Instance of the Bosses class
    defeated = 0  # Number of defeated bosses
    win = False  # Flag indicating if the player has won the game

    # Cache system for backgrounds
    bgCache = {}  # Dictionary to store cached backgrounds
    _cache = {}  # Dictionary to store general cache
    frameRate: int  # Frame rate of the game
    ended = False  # Flag indicating if the game has ended

    def __init__(self):
        pass

    def reset(self):
        """
        Reset the game to its initial state.
        """
        self.loading = True
        self.ready = False

        self.cache("endTick")

        self.player.reset()

        self.grugSprite = grug.Grug(x=self.player.x, y=self.player.y)

        self.player.moveTo(40, 716)
        self.grugSprite.moveTo(*self.player.grugPos("right"))

        self.bosses.load()

        self.tickerRef = monotonic()
        self.ready = True
        self.ended = False
        self.paused = False
        self.render = renderModes.UP
        self._cache = {}
        self.bgIndex = None
        self.mapIndex = 0
        self.defeated = 0
        self.win = False

        self.loading = False

    def setup(self):
        """
        Set up the game.
        """
        self.player = Player.Player()
        self.grugSprite = grug.Grug(x=self.player.x, y=self.player.y)

        self.player.moveTo(40, 716)
        self.grugSprite.moveTo(*self.player.grugPos("right"))

        for file in listdir("./src/assets/bg"):
            name = file.split(".")[0]
            self.bgCache[name] = loadImage(f"./src/assets/bg/{name}.jpg")

        self.tickerRef = monotonic()
        self.bosses.load()
        self.ready = True
        self.loading = False

        if dev:
            self.setBgIndex("guitar")

    def pause(self):
        """
        Pause the game.
        """
        self.paused = True
        self.cache("pauseTick", self.tick)

    def resume(self):
        """
        Resume the game.
        """
        self.paused = False
        self.cache("pauseTick", self.tick)

    def setBgIndex(self, name):
        """
        Set the background index.
        """
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
        """
        Reset the background index.
        """
        self.bgIndex = None
        self.collisions.pop("ground")
        self.render = renderModes.UP
        self.player.setTextureState("idle")

        self.player.moveTo(*self.getcache("beforeCollide"))
        self.cache("beforeCollide")

        self.player.resetPv()

    def cache(self, name, value=None):
        """
        Cache a value.
        """
        if value is None:
            if name in self._cache:
                self._cache.pop(name)
            return self._cache
        self._cache[name] = value
        return value

    def getcache(self, name, default=None):
        """
        Get a cached value.
        """
        return self._cache.get(name, default)

    def startJump(self, coefs=None):
        """
        Start the player's jump.
        """
        self.player.setTextureState("jump")
        self.cache("jumpCoefs", coefs)

        self.player.jumping = True
        self.cache("jumpTick", self.tick)

    def movePlayer(self, *, x=0, y=0, moving=False):
        """
        Move the player.
        """
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
        """
        Cache the background.
        """
        key = self.bgIndex if not self.bgIndex is None else self.mapIndex
        path = f"./src/assets/maps/{self.mapIndex}.jpg" if self.bgIndex is None else f"./src/assets/bg/{self.bgIndex}.jpg"

        if not key in self.bgCache:
            bg = loadImage(path)
            self.bgCache[key] = bg

            return bg
        return self.bgCache[key]

    def checkTriggers(self):
        """
        Check collision triggers.
        """
        if self.collisions["triggers"].inPath(self.player.x, self.player.y):
            scene = self.collisions["triggers"].getId(self.player.x, self.player.y)

            self.setBgIndex(scene)

    def pauseScreen(self):
        """
        Display the pause screen.
        """
        self.grugSprite.display()
        if self.render == renderModes.FACE:
            self.player.display()

        fill(200, 200, 200, 200)
        rect(0, 0, configs["WIDTH"], configs["HEIGHT"])

    def display(self):
        """
        Display the game.
        """
        boss = self.getcache("boss")
        if not not boss and boss.dead:
            self.collisions["triggers"].removeKey(boss.scene)

            self.resetBgIndex()
            self.cache("boss")

            self.defeated += 1
            if self.defeated == len(self.bosses):
                self.ended = True
                self.win = True
                self.cache("endTick", self.tick)
                return

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
                boss.hpBar()

                boss.move(self.player, self, self.tick)
                boss.displayer()

            if self.player.jumping:
                coefs = self.getcache("jumpCoefs")
                if coefs is None:
                    self.player.addJump(self.getcache("jumpTick"), self.tick, self.collisions["ground"].closest(self.player.x, self.player.y)[1])
                else:
                    self.player.addJump(self.getcache("jumpTick"), self.tick, self.collisions["ground"].closest(self.player.x, self.player.y)[1], coefs)
            self.player.hpBar()
        self.player.display()

        self.checkTriggers()

        if self.player.dead:
            self.ended = True
            self.cache("endTick", self.tick)
            return

    @property
    def tick(self):
        """
        Calculate the tick.
        """
        now = monotonic()
        return now - self.tickerRef

    @property
    def playerMoveTexture(self):
        """
        Get the player's move texture.
        """
        return "walk" if self.render == renderModes.UP else "sprint"
