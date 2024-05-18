from typing import List, Callable, Tuple

class Boss:
    pos = (0, 0)
    name: str
    scene: str
    displayer: Callable[[Tuple[float, float], Tuple[float, float]], None]

    # Format: [currentPV, maxPV]
    hp: Tuple[float, float]

    def __init__(self, *, name, scene, hp, pos) -> None:
        self.pos = pos
        self.name = name
        self.scene = scene
        self.hp = [hp, hp]

    def setdisplay(self, displayer):
        self.displayer = displayer

    def display(self):
        self.displayer.display(self.pos, self.hp)
    
    @property
    def dead(self):
        return self.hp[0] <= 0

    def damage(self, amount):
        self.hp[0] = max(self.hp[0] - amount, 0)
        return self.dead