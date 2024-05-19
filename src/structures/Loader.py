from p5 import *
from structures.Timer import Timer
from utils.config import configs

class Loader:
    ended = False
    beforeText = Timer(255)
    step = "prod"
    img = None
    banner = None
    font = None
    ready = False
    clock = 0

    def __init__(self):
        self.beforeText.setTick(1)

    def load(self):
        self.img = loadImage("./src/assets/welcome.png")
        self.banner = loadImage("./src/assets/banner.png")

        self.font = loadFont("./src/assets/fonts/Jaini-Regular.ttf")

    def display(self):
        self.clock += 1

        if not self.beforeText.valid:
            self.beforeText.tick()
        
        if self.step == "prod":
            image(self.banner, 0, 0)

            fill(0, 0, 0, 255 - self.beforeText.tracker)
            rect(0, 0, configs["WIDTH"], configs["HEIGHT"])

            if self.beforeText.valid:
                self.step = "welcome"
                self.beforeText.setTick(1)
        else:
            image(self.img, 0, 0)

            if self.beforeText.valid:
                self.ready = True
            
                fill(250, 101, 120)
                text_font(self.font)
                textSize(45)
                text("Appuyez sur une touche pour continuer...", 865, 812)

    def end(self):
        if self.ended:
            return self
        if self.img:
            del self.img
        if self.font:
            del self.font
        if self.banner:
            del self.banner
        self.ended = True