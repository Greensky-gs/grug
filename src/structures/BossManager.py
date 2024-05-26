from structures.Boss import Boss
from characters.bosses.truck import Truck
from characters.bosses.guitar import Guitar

class Bosses:
    bosses: dict[str, Boss] = {}

    def __init__(self) -> None:
        self.bosses = {}
    def __len__(self) -> int:
        return len(self.bosses)
    
    def load(self):
        self.bosses["truck"] = Truck()
        self.bosses["guitar"] = Guitar()

    def getBoss(self, name: str) -> Boss:
        return self.bosses.get(name)
