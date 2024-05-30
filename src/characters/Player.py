from p5 import *
from utils.config import dev
from methods.parsers import parsePos, parseDirection, horizontal
from methods.paths import Pathing
from structures.Timer import Timer
from math import sin, pi, exp

class Player:
    x = 0  # Position x du joueur
    y = 0  # Position y du joueur

    deltaV = 4  # Vitesse de déplacement normale
    deltaSprint = 2 * deltaV  # Vitesse de déplacement en sprint
    deltaSpeedJump = 1.4 * deltaSprint  # Vitesse de déplacement en saut
    deltaJump = 170  # Hauteur du saut
    deltaGrug = 45  # Distance de déplacement pour l'action "grug"
    jumping: bool = False  # Indique si le joueur est en train de sauter
    shifting = False  # Indique si le joueur est en train de se déplacer en diagonale
    dimens = [0, 0]  # Dimensions de l'image du joueur

    hp = [50, 50]  # Points de vie du joueur

    textures = {
        "walk": {  # Textures pour la marche
            "counter": Timer(8),  # Compteur pour l'animation de la marche
            "textures": []  # Liste des textures de la marche
        },
        "idle": {  # Textures pour l'immobilité
            "counter": Timer(1),  # Compteur pour l'animation de l'immobilité
            "textures": []  # Liste des textures de l'immobilité
        },
        "sprint": {  # Textures pour le sprint
            "counter": Timer(8),  # Compteur pour l'animation du sprint
            "textures": []  # Liste des textures du sprint
        },
        "jump": {  # Textures pour le saut
            "counter": Timer(1),  # Compteur pour l'animation du saut
            "textures": []  # Liste des textures du saut
        },
        "state": "idle"  # État actuel du joueur
    }
    lastDir = "right"  # Dernière direction du joueur

    def __init__(self) -> None:
        for i in range(8):
            walk = loadImage(f"./src/assets/sprites/player/walk/{i}.png")  # Chargement des textures de la marche
            self.textures["walk"]["textures"].append(walk)

            sprint = loadImage(f"./src/assets/sprites/player/sprint/{i}.png")  # Chargement des textures du sprint
            self.textures["sprint"]["textures"].append(sprint)

        self.textures["jump"]["textures"].append(loadImage("./src/assets/sprites/player/jump/0.png"))  # Chargement de la texture du saut
        self.textures["idle"]["textures"].append(loadImage("./src/assets/sprites/player/idle/0.png"))  # Chargement de la texture de l'immobilité
    
    def reset(self):
        self.x = 0  # Réinitialisation de la position x du joueur
        self.y = 0  # Réinitialisation de la position y du joueur

        self.jumping = False  # Réinitialisation de l'état de saut du joueur
        self.shifting = False  # Réinitialisation de l'état de déplacement en diagonale du joueur
        self.hp = [self.hp[1], self.hp[1]]  # Réinitialisation des points de vie du joueur
        self.lastDir = "right"  # Réinitialisation de la dernière direction du joueur

        self.textures["state"] = "idle"  # Réinitialisation de l'état actuel du joueur
        for key in self.textures:
            if key == "state":
                continue
            self.textures[key]["counter"].reset()  # Réinitialisation des compteurs d'animation

    def setTextureState(self, state):
        if state == self.textures["state"]:
            return

        self.textures[state]["counter"].reset()  # Réinitialisation du compteur d'animation pour l'état donné

        self.textures["state"] = state  # Mise à jour de l'état actuel du joueur

    def hpBar(self):
        ox = 33  # Position x de la barre de vie
        oy = 789  # Position y de la barre de vie

        width = 270  # Largeur de la barre de vie
        height = 10  # Hauteur de la barre de vie
        outline = 2  # Épaisseur de la bordure de la barre de vie

        noStroke()
        fill(0)
        rect(ox, oy, width + outline * 2, height + outline * 2)  # Dessin du fond de la barre de vie

        fill(125)
        rect(ox + outline, oy + outline, width, height)  # Dessin de la barre de vie

        fill(6, 180, 59)
        rect(ox + outline, oy + outline, max(0, width * (self.hp[0] / self.hp[1])), height)  # Dessin de la partie remplie de la barre de vie en fonction des points de vie actuels du joueur

    @property
    def delta(self):
        return self.deltaSprint if self.textures["state"] == "sprint" else self.deltaSpeedJump if self.jumping else self.deltaV  # Calcul de la vitesse de déplacement en fonction de l'état du joueur

    def move(self, x, y, *, paths: Pathing):
        pos = parsePos(self.x + x * self.delta, self.y + y * self.delta)  # Calcul de la nouvelle position du joueur

        if horizontal(parseDirection(x, y)):
            self.lastDir = parseDirection(x, y)  # Mise à jour de la dernière direction du joueur

        if not paths.inPath(pos[0], pos[1]):
            pos = paths.closest(pos[0], pos[1])  # Si la nouvelle position n'est pas dans le chemin, on déplace le joueur vers la position la plus proche dans le chemin

            if abs(pos[0] - self.x) > 10 or abs(pos[1] - self.y) > 10:
                pos = parsePos(self.x, self.y)  # Si la distance entre la nouvelle position et la position actuelle est trop grande, on reste à la position actuelle

        self.x, self.y = pos  # Mise à jour de la position du joueur

    def resetPv(self):
        self.hp[0] = self.hp[1]  # Réinitialisation des points de vie actuels du joueur
        return self

    @property
    def pos(self):
        return (self.x, self.y)  # Renvoie la position du joueur

    def grugPos(self, direction):
        return [
            self.x + (self.deltaGrug if direction == "left" else -self.deltaGrug if direction == "right" else 0),  # Calcul de la position x pour l'action "grug"
            self.y + (self.deltaGrug if direction == "up" else -self.deltaGrug if direction == "down" else 0)  # Calcul de la position y pour l'action "grug"
        ]

    def addJump(self, startTick, currentTick, c, coefs = [0.7, 0.8, -1.1]):
        absis = (currentTick - startTick)

        a, t, l = coefs

        jump = lambda x: (a * sin((pi * x)/t) * exp(-l * x))  # Fonction de saut

        y = min(jump(absis) * self.deltaJump * -1, 0)  # Calcul de la hauteur du saut

        if y >= 0 and startTick != currentTick:
            self.jumping = False  # Si la hauteur du saut est supérieure ou égale à 0 et que le tick de début est différent du tick actuel, le joueur a terminé son saut
        self.y = y + c  # Mise à jour de la position y du joueur

    def tickTexture(self):
        self.textures[self.textures["state"]]["counter"].tick()  # Incrémentation du compteur d'animation

    def hitbox(self, w, h):
        fill(255)
        rect(self.x, self.y, w, h)  # Dessin de la hitbox du joueur

    def damage(self, amount):
        self.hp[0] = max(self.hp[0] - amount, 0)  # Réduction des points de vie du joueur en fonction du montant de dégâts reçus
        return self.dead  # Renvoie True si le joueur est mort, False sinon

    @property
    def dead(self):
        return self.hp[0] <= 0  # Renvoie True si le joueur est mort, False sinon

    def display(self):
        texture = self.textures[self.textures["state"]]
        img = texture["textures"][texture["counter"].count]  # Récupération de la texture à afficher

        self.dimens = [img.width, img.height]  # Mise à jour des dimensions de l'image du joueur

        if dev:
            self.hitbox(img.width, -img.height)  # Affichage de la hitbox du joueur en mode développement
        pushMatrix()

        translate(self.x, self.y)

        coef = 0
        if self.lastDir == "left":
            scale(-1, 1)
            coef = -1
        image(img, img.width * coef, -img.height)  # Affichage de l'image du joueur

        popMatrix()

    def moveTo(self, x, y):
        self.x, self.y = parsePos(x, y)  # Déplacement du joueur vers une position donnée

    @property
    def width(self):
        return self.dimens[0]  # Renvoie la largeur de l'image du joueur

    @property
    def height(self):
        return self.dimens[1]  # Renvoie la hauteur de l'image du joueur
