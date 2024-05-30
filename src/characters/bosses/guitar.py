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
    direction: DirectionType  # Direction de l'attaque
    pos = [0, 0]  # Position de l'attaque (en haut à gauche)
    texture: Any  # Texture de l'attaque
    width = randint(50, 100)  # Largeur de l'attaque (aléatoire entre 50 et 100)
    height = randint(80, 145)  # Hauteur de l'attaque (aléatoire entre 80 et 145)
    damage = randint(3, 5)  # Dommages de l'attaque (aléatoire entre 3 et 5)
    deltaV = randint(5, 10)  # Vitesse de déplacement de l'attaque (aléatoire entre 5 et 10)
    creation: int  # Instant de création de l'attaque

    def __init__(self, *, direction: DirectionType, pos = [0, 0], ground: int, tick: int) -> None:
        """
        Initialise une instance de l'attaque de guitare.

        Args:
            direction (DirectionType): La direction de l'attaque.
            pos (List[int], optional): La position de l'attaque. Defaults to [0, 0].
            ground (int): La position au sol de l'attaque.
            tick (int): L'instant de création de l'attaque.
        """
        self.direction = direction
        self.pos = pos
        self.creation = tick

        self.pos[1] = ground - self.height

        self.texture = loadImage("src/assets/sprites/bosses/guitar/attack.png")

    
    def display(self):
        """
        Affiche l'attaque de guitare à l'écran.
        """
        pushMatrix()

        translate(*self.pos)

        image(self.texture, 0, 0, self.width, self.height)

        popMatrix()

    def move(self):
        """
        Déplace l'attaque de guitare en fonction de sa direction.
        """
        if self.direction == "right":
            self.pos[0] += self.deltaV
        else:
            self.pos[0] -= self.deltaV

        # Vérification de collision avec les bords de l'écran
        if self.pos[0] <= 0 or self.pos[0] + self.width >= configs["WIDTH"]:
            self.direction = oppositeDirection(self.direction)

class Guitar(Boss):
    texture: Any  # Texture de la guitare
    lastDir = "left"  # Dernière direction de déplacement de la guitare
    cache = Cache()  # Cache pour stocker des données temporaires
    width = None  # Largeur de la guitare
    height = None  # Hauteur de la guitare
    deltaDamage = 2  # Variation des dommages infligés par la guitare
    deltaV = 7  # Vitesse de déplacement de la guitare
    evolved = False  # Indicateur d'évolution de la guitare

    def __init__(self) -> None:
        """
        Initialise une instance du boss Guitar.
        """
        super().__init__(name = "Guitare", scene="guitar", hp=70, pos = (800, 698))

        self.texture = loadImage("src/assets/sprites/bosses/guitar/guitar.png")

        self.width = self.texture.width
        self.height = self.texture.height

        def display():
            """
            Affiche la guitare à l'écran.
            """
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
    
    def damage(self, damage: int):
        """
        Inflige des dommages à la guitare.

        Args:
            damage (int): Les dommages à infliger.
        """
        self.hp[0] -= damage
        if self.hp[0] <= 0:
            self.hp[0] = 0
        if self.hp[0] <= 0.5 * self.hp[1]:
            self.evolve()
    
    def hpBar(self):
        """
        Affiche la barre de vie de la guitare.
        """
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
        """
        Gère l'attaque de la guitare à chaque tick.

        Args:
            player (Player): Le joueur.
            tick (int): Le tick actuel.
        """
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
                self.damage(attack.damage)
            if checkCollision(oxa=player.x, oya=player.y - player.height, wa=player.width, ha=player.height, oxb=attack.pos[0], oyb=attack.pos[1], wb=attack.width, hb=attack.height):
                player.damage(attack.damage)
                self.cache.delete("attack")
    
    def evolve(self):
        """
        Fait évoluer la guitare.
        """
        if not self.evolved:
            self.deltaV = int(self.deltaV * 1.5)
            self.evolved = True

    @property
    def dead(self):
        """
        Vérifie si la guitare est morte.

        Returns:
            bool: True si la guitare est morte, False sinon.
        """
        return self.hp[0] <= 0
    
    def setPos(self, player: Player, game, tick: int):
        """
        Définit la position de la guitare en fonction du joueur.

        Args:
            player (Player): Le joueur.
            game: Le jeu.
            tick (int): Le tick actuel.
        """
        okTick = self.cache.get("okTick")
        if not not okTick and tick < okTick:
            return
        self.cache.delete("okTick")

        target = self.cache.get("target")

        if not target:
            target = (player.x, self.pos[1])
            self.cache.cache("target", target)
        
        current = list(self.pos).copy()
        if self.pos[0] < target[0]:
            current[0] += self.deltaV
            self.lastDir = "right"
        elif self.pos[0] > target[0]:
            current[0] -= self.deltaV
            self.lastDir = "left"
        
        if abs(self.pos[0] - target[0]) <= self.width:
            self.cache.delete("target")
            okTick = tick + randint(1, 3)
            self.cache.cache("okTick", okTick)

        self.pos = tuple(current)
    
    def move(self, player: Player, game, tick: int):
        """
        Gère le mouvement de la guitare.

        Args:
            player (Player): Le joueur.
            game: Le jeu.
            tick (int): Le tick actuel.
        """
        self.tickAttack(player, tick)
        self.setPos(player, game, tick)

        self.pos = parsePos(*self.pos, aw=self.width)
