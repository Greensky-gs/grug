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
        # Charger les boss dans le dictionnaire
        self.bosses["truck"] = Truck()  # Ajouter un boss de type Truck
        self.bosses["guitar"] = Guitar()  # Ajouter un boss de type Guitar

    def getBoss(self, name: str) -> Boss:
        # Récupérer un boss à partir de son nom
        return self.bosses.get(name)
