class Timer:
    mod: int = 0
    tracker: int = 0

    def __init__(self, mod: int) -> None:
        self.mod = mod
    
    def tick(self):
        self.tracker = (self.tracker + 1) % self.mod
        return self.valid
    
    def reset(self):
        self.tracker = 0

    def setTick(self, tick: int):
        self.tracker = tick % self.mod
    @property
    def valid(self):
        return self.tracker == 0
    
    @property
    def count(self):
        return self.tracker