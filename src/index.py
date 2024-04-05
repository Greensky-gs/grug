from utils.config import configs
from p5 import *
from structures.Game import Game

game = Game()

def setup():
    size(configs["WIDTH"], configs["HEIGHT"])

def draw():
    background(0)
    game.display()

def key_pressed():
    keysLeft = ["a", "q", "LEFT"]
    keysRight = ["d", "RIGHT"]
    keysUp = ["z", "UP", "w"]
    keysDown = ["DOWN", "s"]
    combined = keysLeft + keysRight + keysUp + keysDown


    if key in combined:
        xMov = 0 if not key in keysLeft + keysRight else (1 if key in keysRight else -1)
        yMov = 0 if not key in keysUp + keysDown else (-1 if key in keysUp else 1)

        game.player.move(x = xMov, y = yMov)


run()