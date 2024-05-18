from structures.Boss import Boss
from structures.Cache import Cache
from characters.Player import Player
from structures.Timer import Timer
from typing import Any
from utils.config import configs, dev
from methods.parsers import parseDirection, parsePos
from p5 import *
from random import randint

class Truck(Boss):
    texture: Any
    lastDir = "left"
    cache = Cache()
    width = None
    height = None
    deltaDamage = 2

    def __init__(self) -> None:
        super().__init__(name = "Truck", scene="truck", hp=100, pos = (800, 667))

        self.texture = loadImage("./src/assets/sprites/bosses/truck/truck.png")

        self.width = self.texture.width
        self.height = self.texture.height

        self.cache.cache("damageTicker", Timer(60))

        def display():
            self.cache.get("damageTicker").tick()

            if self.cache.get("damageTicker").valid:
                self.damage(self.deltaDamage)

            if dev:
                fill(255)
                rect(*self.pos, self.width, -self.height)

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
    def move(self, player: Player, tick: int):
        self.setPos(player, tick)
        self.pos = parsePos(*self.pos, aw=self.width)

        return self.pos
    def setPos(self, player: Player, tick: int):
        def clearCache():
            self.cache.delete("target")
            self.cache.delete("tick")
            self.cache.delete("timeout")
            self.cache.delete("operand")

        if self.cache.get("waiting"):
            if tick - self.cache.get("waiting") < 1.3:
                coef = -1 if player.x > self.pos[0] else 1

                self.pos = (self.pos[0] + randint(3, 6) * coef, self.pos[1])
                return
            else:
                self.cache.delete("waiting")

        if not self.cache.get("target"):
            if self.pos[0] >= configs["WIDTH"] // 2:
                self.cache.cache("target", (0, self.pos[1]))
                self.cache.cache("operand", "<=")
            else:
                self.cache.cache("operand", ">=")
                self.cache.cache("target", (configs["WIDTH"] - self.width, self.pos[1]))

            self.cache.cache("tick", tick)
            self.cache.cache("timeout", randint(10, 20) / 10)
        else:
            start = self.cache.get("tick")
            target = self.cache.get("target")

            coef = 1 if target[0] > self.pos[0] else -1

            if tick - start < self.cache.get("timeout"):
                self.pos = (self.pos[0] - 10 * coef, self.pos[1])
            else:
                self.pos = (self.pos[0] + 20 * coef, self.pos[1])
            
            self.lastDir = parseDirection(coef, 0)
        if eval(f"{self.pos[0]} {self.cache.get('operand')} {self.cache.get('target')[0]}"):
            clearCache()

            self.cache.cache("waiting", tick)
        if self.pos[0] < player.pos[0] + 50 and self.pos[0] + 50 > player.pos[0] and self.pos[1] < player.pos[1] + 50 and self.pos[1] + 50 > player.pos[1]:
            # self.cache.delete("target")
            # self.cache.delete("tick")
            # self.cache.delete("timeout")

            # self.cache.cache("waiting", tick)
            # TODO ajouter les collisions
            pass
