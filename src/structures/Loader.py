from p5 import *
from structures.Timer import Timer
from utils.config import configs

class Loader:
    # Variable to track if the loader has ended
    ended = False
    # Timer for the before text animation
    beforeText = Timer(255)
    # Current step of the loader
    step = "prod"
    # Images used in the loader
    img = None
    banner = None
    winImg = None
    # Font used in the loader
    font = None
    # Image displayed when the game is lost
    lost = None
    # Flag to indicate if the loader is ready
    ready = False
    # Clock to keep track of time
    clock = 0

    def __init__(self):
        # Set the tick for the before text animation
        self.beforeText.setTick(1)

    def load(self):
        # Load the images and font used in the loader
        self.img = loadImage("./src/assets/welcome.png")
        self.banner = loadImage("./src/assets/banner.png")
        self.lost = loadImage("./src/assets/lost.png")
        self.winImg = loadImage("./src/assets/win_screen.png")

        self.font = loadFont("./src/assets/fonts/Jaini-Regular.ttf")

    def win(self):
        # Display the win screen image
        image(self.winImg, 0, 0)

    def display(self):
        # Increment the clock
        self.clock += 1

        if not self.beforeText.valid:
            # Tick the before text animation
            self.beforeText.tick()

        if self.step == "prod":
            # Display the banner image
            image(self.banner, 0, 0)

            # Fade out the screen with a black rectangle
            fill(0, 0, 0, 255 - self.beforeText.tracker)
            rect(0, 0, configs["WIDTH"], configs["HEIGHT"])

            if self.beforeText.valid:
                # If the before text animation is finished, move to the next step
                self.step = "welcome"
                self.beforeText.setTick(1)
        else:
            # Display the welcome image
            image(self.img, 0, 0)

            if self.beforeText.valid:
                # Set the ready flag to indicate that the loader is ready
                self.ready = True

                # Display the text to prompt the user to continue
                fill(250, 101, 120)
                text_font(self.font)
                textSize(45)
                text("Appuyez sur une touche pour continuer...", 865, 812)

    def end(self):
        if self.ended:
            return self
        if self.img:
            # Delete the image to free up memory
            del self.img
        if self.banner:
            # Delete the banner image to free up memory
            del self.banner
        self.ended = True

    def lostScreen(self):
        # Display the lost screen image
        image(self.lost, 0, 0)

        message = "Appuyez sur une touche pour recommencer..."

        fill(250, 101, 120)
        text_font(self.font)
        textSize(45)
        text(message, configs["WIDTH"] / 2 - (len(message) / 2) * 15, configs["HEIGHT"] / 2 - 22)