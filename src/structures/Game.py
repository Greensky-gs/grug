from characters import grug
from characters import Player
from structures.Character import Character
from utils.config import configs
from methods.parsers import parseDirection, horizontal
from methods.paths import Pathing
from p5 import loadImage, image

class Game:
    player: Player.Player
    grugSprite: grug.Grug
    mapIndex = 0
    paths = Pathing()

    # Système de cache pour les arrières-plans
    bgCache = {}

    def __init__(self):
        pass
    
    def setup(self):
        self.player = Player.Player()
        self.grugSprite = grug.Grug(x = self.player.x, y = self.player.y)

        self.player.moveTo(40, 716)
        self.grugSprite.moveTo(*self.player.grugPos("right"))

    def movePlayer(self, *, x = 0, y = 0, moving = False):
        if moving:
            self.player.setTextureState("walk")
            self.grugSprite.setTextureState("walk")
        else:
            self.player.setTextureState("idle")
            self.grugSprite.setTextureState("idle")

        self.player.tickTexture()

        self.player.move(x, y, self.paths)
        
        lastDir = parseDirection(x, y)

        if horizontal(lastDir):
            self.grugSprite.setLastX(lastDir)
        self.grugSprite.setLastDirection(lastDir)
        self.grugSprite.moveTo(*self.player.grugPos(self.grugSprite.lastDirection))

    def bgCaching(self):
        if not self.mapIndex in self.bgCache:
            bg = loadImage(f"./src/assets/maps/{self.mapIndex}.jpg")
            self.bgCache[self.mapIndex] = bg

            return bg
        return self.bgCache[self.mapIndex]    

    def display(self):
        bg = self.bgCaching()
        image(bg, 0, 0)

        self.grugSprite.display()
        self.player.display()