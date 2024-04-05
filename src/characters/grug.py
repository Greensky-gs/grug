from structures.Character import Character

class Grug:
    name = "Grug"
    pos = [0, 0]
    pnj: Character;

    def __init__(self, *, x, y) -> None:
        self.pos = [x, y]
        self.pnj = Character(x = self.pos[0], y = self.pos[1], name = self.name)

        def drawer(x, y):
            pass
        self.pnj.setDrawer(drawer)

    def display(self):
        self.pnj.display()