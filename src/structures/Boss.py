from typing import List, Callable, Tuple

class Boss:
    pos = (0, 0)  # Position du boss sur la scène
    name: str  # Nom du boss
    scene: str  # Scène dans laquelle le boss se trouve
    displayer: Callable[[Tuple[float, float], Tuple[float, float]], None]  # Fonction d'affichage du boss

    # Format: [currentPV, maxPV]
    hp: Tuple[float, float]  # Points de vie actuels et maximum du boss

    def __init__(self, *, name, scene, hp, pos) -> None:
        self.pos = pos
        self.name = name
        self.scene = scene
        self.hp = [hp, hp]

    def setdisplay(self, displayer):
        """
        Définit la fonction d'affichage du boss.
        :param displayer: Fonction d'affichage
        """
        self.displayer = displayer

    def display(self):
        """
        Affiche le boss en utilisant la fonction d'affichage définie.
        """
        self.displayer.display(self.pos, self.hp)
    
    @property
    def dead(self):
        """
        Vérifie si le boss est mort.
        :return: True si le boss est mort, False sinon
        """
        return self.hp[0] <= 0

    def damage(self, amount):
        """
        Inflige des dégâts au boss.
        :param amount: Montant des dégâts
        :return: True si le boss est mort après les dégâts, False sinon
        """
        self.hp[0] = max(self.hp[0] - amount, 0)
        return self.dead

    @property
    def x(self):
        """
        Renvoie la coordonnée x de la position du boss.
        :return: Coordonnée x
        """
        return self.pos[0]
    
    @property
    def y(self):
        """
        Renvoie la coordonnée y de la position du boss.
        :return: Coordonnée y
        """
        return self.pos[1]