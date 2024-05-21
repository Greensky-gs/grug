from utils.config import configs, renderModes
from p5 import *
from structures.Game import Game
from structures.Loader import Loader

game = Game()
loader = Loader()

def setup():
    size(configs["WIDTH"], configs["HEIGHT"])

    game.setup()
    loader.load()

def draw():
    background(0)

    if not loader.ended:
        loader.display()

        if loader.ready and key_is_pressed:
            loader.end()
        return

    if not game.ready:
        return

    if game.player.dead or not game.ready:
        loader.lostScreen()

        if game.tick - game.getcache("endTick", -100) > 3 and key_is_pressed and not game.loading:
            game.reset()
        return

    # Gère mouvements du joueur
    if key_is_pressed:
        keysLeft = ["a", "q", "left"]
        keysRight = ["d", "right"]
        keysUp = ["z", "up", "w"]
        keysDown = ["down", "s"]
        combined = keysLeft + keysRight + keysUp + keysDown

        pressedKey = str(key).lower()

        if pressedKey == "backspace":
            pauseTick = game.getcache('pauseTick')
            if pauseTick is None:
                game.pause()
                return
            else:
                if game.tick - pauseTick >= 1:
                    if game.paused:
                        game.resume()
                    else:
                        game.pause()
                    return

        xMov = 0
        yMov = 0
        if pressedKey in combined:
            xMov = 0 if not pressedKey in keysLeft + keysRight else (1 if pressedKey in keysRight else -1)
            yMov = 0 if not pressedKey in keysUp + keysDown else (-1 if pressedKey in keysUp else 1)

        if not game.paused:
            game.movePlayer(x = xMov, y = yMov, moving=xMov!= 0 or yMov!= 0)
        if game.render == renderModes.FACE:
            if pressedKey in keysUp + [" "] and not game.player.jumping:
                game.startJump()
    else:
        if not game.player.jumping:
            game.grugSprite.setTextureState("idle")
            game.player.setTextureState("idle")
    
    if mouse_is_pressed:
        if game.render == renderModes.FACE and not game.player.jumping:
            game.startJump()
    game.display()


run()