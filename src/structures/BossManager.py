from structures.Boss import Boss
from characters.bosses.truck import Truck

class Bosses:
    bosses: dict[str, Boss] = {}

    def __init__(self) -> None:
        self.bosses = {}
    
    def load(self):
        self.bosses["truck"] = Truck()

    def getBoss(self, name: str) -> Boss:
        return self.bosses.get(name)
