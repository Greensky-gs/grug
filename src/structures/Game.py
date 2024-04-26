from characters import grug
from characters import Player
from structures.Character import Character
from utils.config import configs

class Game:
    player: Player.Player
    grugSprite: grug.Grug
    mapIndex = 0

    def __init__(self):
        self.player = Player.Player()
        self.grugSprite = grug.Grug(x = self.player.x, y = self.player.y)

    def movePlayer(self, *, x = 0, y = 0):
        self.player.move(x, y)
        
        lastDir = None
        if x != 0:
            lastDir = "left" if x < 0 else "right"
        else:
            lastDir = "up" if y < 0 else "down"

        self.grugSprite.setLastDirection(lastDir)
        self.grugSprite.moveTo(*self.player.grugPos(self.grugSprite.lastDirection))

    def display(self):
        self.grugSprite.display()
        self.player.display()