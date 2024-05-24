from structures.Boss import Boss
from typing import Any
from structures.Cache import Cache
from p5 import *
from utils.config import dev

class Guitar(Boss):
    texture: Any
    lastDir = "left"
    cache = Cache()
    width = None
    height = None
    deltaDamage = 2

    def __init__(self) -> None:
        super().__init__(name = "Guitare", scene="guitar", hp=70, pos = (800, 698))

        self.texture = loadImage("src/assets/sprites/bosses/guitar/guitar.png")

        self.width = self.texture.width
        self.height = self.texture.height

        def display():
            pushMatrix()

            translate(*self.pos)

            coef = 0
            if self.lastDir == "left":
                scale(-1, 1)
                coef = -1
            image(self.texture, self.width * coef, -self.height)

            popMatrix()

        self.setdisplay(display)
    
    def hpBar(self):
        width = 320
        outline = 5
        height = 15

        ox = 10
        oy = 10

        noStroke()
        fill(0)
        rect(ox, oy, width + outline * 2, height + outline * 2)

        fill(125)
        rect(ox + outline, oy + outline, width, height)

        fill(255, 0, 0)
        rect(ox + outline, oy + outline, max(0, width * (self.hp[0] / self.hp[1])), height)
    def launchAttack(self):
        pass
    def move(self, player, game, tick):
        pass