from p5 import *
from structures.Timer import Timer

class Loader:
    ended = False
    beforeText = Timer(240)
    img = None
    font = None
    ready = False

    def __init__(self):
        self.beforeText.setTick(1)
        pass

    def load(self):
        self.img = loadImage("./src/assets/welcome.png")

        # Q: How to load a font ?
        # A: You can load a font by using the loadFont() function.
        #    Here is an example:
        #    font = loadFont("path/to/font.ttf")
        #    text_font(font)
        self.font = loadFont("./src/assets/fonts/Jaini-Regular.ttf")

    def display(self):
        if not self.beforeText.valid:
            self.beforeText.tick()
        
        image(self.img, 0, 0)

        if self.beforeText.valid:
            self.ready = True
            
            fill(250, 101, 120)
            text_font(self.font)
            textSize(45)
            text("Appuyez sur une touche pour continuer...", 865, 812)
    
    def end(self):
        self.ended = True