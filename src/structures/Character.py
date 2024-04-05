class Character:
    drawer = None
    pos = [0, 0]
    name = None

    def __init__(self, *, x, y, name) -> None:
        self.name = name
        self.pos = [x, y]
    
    def setDrawer(self, drawer):
        self.drawer = drawer;
    
    def display(self):
        self.drawer(*self.pos)