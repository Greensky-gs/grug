from characters import grug, Player
from structures.Character import Character

class Game:
    player: Player.Player
    grug: grug.Grug
    mapIndex = 0

    def __init__(self):
        self.player = Player.Player()
        self.grug = grug.Grug(x = self.player.x, y = self.player.y)
    
    def display(self):
        self.player.display()