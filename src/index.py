from utils.config import configs
from p5 import *
from structures.Game import Game

game = Game()

def setup():
    size(configs["WIDTH"], configs["HEIGHT"])


def draw():
    resetMatrix()
    scale(1)
    background(0)

    # Gère mouvements du joueur
    if key_is_pressed:
        keysLeft = ["a", "q", "left"]
        keysRight = ["d", "right"]
        keysUp = ["z", "up", "w"]
        keysDown = ["down", "s"]
        combined = keysLeft + keysRight + keysUp + keysDown

        pressedKey = str(key).lower()

        xMov = 0
        yMov = 0
        if pressedKey in combined:
            xMov = 0 if not pressedKey in keysLeft + keysRight else (1 if pressedKey in keysRight else -1)
            yMov = 0 if not pressedKey in keysUp + keysDown else (-1 if pressedKey in keysUp else 1)

        game.movePlayer(x = xMov, y = yMov)


    game.display()


run()