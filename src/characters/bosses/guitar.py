from structures.Boss import Boss
from typing import Any, List
from structures.Cache import Cache
from p5 import *
from utils.config import dev, configs
from methods.parsers import DirectionType, parsePos, oppositeDirection, checkCollision, randomDirection
from random import randint
from structures.Timer import Timer
from characters.Player import Player

class GuitarAttack:
    direction: DirectionType
    # Position à partir d'en haut à gauche
    pos = [0, 0]
    texture: Any
    width = randint(50, 100)
    height = randint(80, 160)
    damage = randint(3, 5)
    deltaV = randint(5, 10)
    creation: int

    def __init__(self, *, direction: DirectionType, pos = [0, 0], ground: int, tick: int) -> None:
        self.direction = direction
        self.pos = pos
        self.creation = tick

        self.pos[1] = ground - self.height

        self.texture = loadImage("src/assets/sprites/bosses/guitar/attack.png")

    
    def display(self):
        pushMatrix()

        translate(*self.pos)

        image(self.texture, 0, 0, self.width, self.height)

        popMatrix()

    def move(self):
        if self.direction == "right":
            self.pos[0] += self.deltaV
        else:
            self.pos[0] -= self.deltaV

        # Vérification de collision avec les bords de l'écran
        if self.pos[0] <= 0 or self.pos[0] + self.width >= configs["WIDTH"]:
            self.direction = oppositeDirection(self.direction)

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

            attack: GuitarAttack = self.cache.get("attack")
            if attack:
                attack.display()

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
    def tickAttack(self, player: Player, tick: int):
        if not self.cache.get("attack"):
            timer = self.cache.get("beforeAttack")
            if not timer:
                timer = Timer(randint(1, 3) * 60)
                timer.setTick(1)
                self.cache.cache("beforeAttack", timer)
            
            timer.tick()
            if timer.valid:
                self.cache.delete("beforeAttack")
                
                attack = GuitarAttack(direction=randomDirection(["down", "up"]), pos=list(self.pos).copy(), ground=self.pos[1], tick=tick)
                self.cache.cache("attack", attack)
        else:
            attack: GuitarAttack = self.cache.get("attack")

            attack.move()
            attack.display()

            if tick - attack.creation > 1 and checkCollision(oxa=self.pos[0], oya=self.pos[1] - self.height, wa=self.width, ha=self.height, oxb=attack.pos[0], oyb=attack.pos[1], wb=attack.width, hb=attack.height):
                self.cache.delete("attack")
                self.hp[0] -= attack.damage
            if checkCollision(oxa=player.x, oya=player.y - player.height, wa=player.width, ha=player.height, oxb=attack.pos[0], oyb=attack.pos[1], wb=attack.width, hb=attack.height):
                player.damage(attack.damage)
                self.cache.delete("attack")
    
    @property
    def dead(self):
        return self.hp[0] <= 0
    def setPos(self, player: Player, game, tick: int):
        pass
    def move(self, player: Player, game, tick: int):
        self.tickAttack(player, tick)
        self.setPos(player, game, tick)

        self.pos = parsePos(*self.pos, aw=self.width)