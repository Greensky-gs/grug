class Timer:
    mod: int = 0  # Modulo utilisé pour le suivi du temps
    tracker: int = 0  # Variable de suivi du temps

    def __init__(self, mod: int) -> None:
        self.mod = mod
    
    def tick(self):
        """
        Incrémente le suivi du temps et retourne si le temps est valide.
        """
        self.tracker = (self.tracker + 1) % self.mod
        return self.valid
    
    def reset(self):
        """
        Réinitialise le suivi du temps à zéro.
        """
        self.tracker = 0

    def setTick(self, tick: int):
        """
        Définit la valeur du suivi du temps.
        """
        self.tracker = tick % self.mod
    
    @property
    def valid(self):
        """
        Vérifie si le temps est valide (tracker == 0).
        """
        return self.tracker == 0
    
    @property
    def count(self):
        """
        Retourne la valeur actuelle du suivi du temps.
        """
        return self.tracker