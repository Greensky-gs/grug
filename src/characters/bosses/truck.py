from structures.Boss import Boss
from structures.Cache import Cache
from characters.Player import Player
from structures.Timer import Timer
from typing import Any
from utils.config import configs, dev
from methods.parsers import parseDirection, parsePos, checkCollision
from p5 import *
from random import randint

class Truck(Boss):
    texture: Any  # Texture du camion
    lastDir = "left"  # Dernière direction du camion
    cache = Cache()  # Cache pour stocker des données temporaires
    width = None  # Largeur du camion
    height = None  # Hauteur du camion
    deltaDamage = 2  # Dommage infligé par le camion

    def __init__(self) -> None:
        super().__init__(name="Truck", scene="truck", hp=100, pos=(800, 667))

        self.texture = loadImage("./src/assets/sprites/bosses/truck/truck.png")  # Chargement de la texture du camion

        self.width = self.texture.width  # Récupération de la largeur de la texture
        self.height = self.texture.height  # Récupération de la hauteur de la texture

        self.cache.cache("damageTicker", Timer(60))  # Initialisation du timer pour les dégâts

        def display():
            self.cache.get("damageTicker").tick()  # Incrémentation du timer pour les dégâts

            if self.cache.get("damageTicker").valid:
                self.damage(self.deltaDamage)  # Infliger des dégâts au joueur

            if dev:
                fill(255)
                rect(*self.pos, self.width, -self.height)  # Affichage du camion en mode développeur

            pushMatrix()

            translate(*self.pos)

            coef = 0
            if self.lastDir == "left":
                scale(-1, 1)
                coef = -1
            image(self.texture, self.width * coef, -self.height)  # Affichage du camion

            popMatrix()

        self.setdisplay(display)  # Définition de la fonction d'affichage

    def hpBar(self):
        width = 320  # Largeur de la barre de vie
        outline = 5  # Épaisseur de la bordure
        height = 15  # Hauteur de la barre de vie

        ox = 10  # Position x du coin supérieur gauche de la barre de vie
        oy = 10  # Position y du coin supérieur gauche de la barre de vie

        noStroke()
        fill(0)
        rect(ox, oy, width + outline * 2, height + outline * 2)  # Affichage du contour de la barre de vie

        fill(125)
        rect(ox + outline, oy + outline, width, height)  # Affichage de la barre de vie

        fill(255, 0, 0)
        rect(ox + outline, oy + outline, max(0, width * (self.hp[0] / self.hp[1])), height)  # Affichage de la barre de vie remplie

    def move(self, player: Player, game, tick: int):
        self.setPos(player, game, tick)  # Déplacement du camion
        self.pos = parsePos(*self.pos, aw=self.width)  # Analyse de la position du camion

        return self.pos

    def setPos(self, player: Player, game, tick: int):
        def clearCache():
            self.cache.delete("target")
            self.cache.delete("tick")
            self.cache.delete("timeout")
            self.cache.delete("operand")
            self.cache.delete("damager")

        if self.cache.get("waiting"):
            if tick - self.cache.get("waiting") < 1.3:
                coef = -1 if player.x > self.pos[0] else 1

                self.pos = (self.pos[0] + randint(3, 6) * coef, self.pos[1])  # Déplacement du camion en attente
                return
            else:
                self.cache.delete("waiting")

        if not self.cache.get("target"):
            if self.pos[0] >= configs["WIDTH"] // 2:
                self.cache.cache("target", (0, self.pos[1]))  # Définition de la cible du camion
                self.cache.cache("operand", "<=")
            else:
                self.cache.cache("operand", ">=")
                self.cache.cache("target", (configs["WIDTH"] - self.width, self.pos[1]))  # Définition de la cible du camion

            self.cache.cache("tick", tick)
            self.cache.cache("timeout", randint(10, 20) / 10)
            self.cache.cache("damager", Timer(45))

            self.cache.get("damager").setTick(43)
        else:
            start = self.cache.get("tick")
            target = self.cache.get("target")

            coef = 1 if target[0] > self.pos[0] else -1

            if tick - start < self.cache.get("timeout"):
                self.pos = (self.pos[0] - 10 * coef, self.pos[1])  # Déplacement du camion vers la cible
            else:
                self.pos = (self.pos[0] + 20 * coef, self.pos[1])  # Déplacement du camion après avoir atteint la cible
            
            self.lastDir = parseDirection(coef, 0)  # Mise à jour de la dernière direction du camion

            if checkCollision(oxa=self.x, oya=self.y, oxb=player.x, oyb=player.y, wa=self.width, ha=self.height, wb=player.width, hb=player.height):
                self.cache.get("damager").tick()  # Incrémentation du timer pour les dégâts
                if self.cache.get("damager").valid:
                    player.damage(8 if not dev else 2000)  # Infliger des dégâts au joueur
                    game.startJump([2.6, 0.8, 1.7])  # Déclenchement du saut du joueur

        if eval(f"{self.pos[0]} {self.cache.get('operand')} {self.cache.get('target')[0]}"):
            clearCache()

            self.cache.cache("waiting", tick)  # Mise en attente du camion
        if self.pos[0] < player.pos[0] + 50 and self.pos[0] + 50 > player.pos[0] and self.pos[1] < player.pos[1] + 50 and self.pos[1] + 50 > player.pos[1]:
            # self.cache.delete("target")
            # self.cache.delete("tick")
            # self.cache.delete("timeout")

            # self.cache.cache("waiting", tick)
            # TODO ajouter les collisions
            pass
