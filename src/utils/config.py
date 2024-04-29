from sys import argv

configs = {
    "WIDTH": 1500,
    "HEIGHT": 900,
    "loadingTime": 200
}

class RenderModes:
    UP = "up",
    FACE = "face"

renderModes = RenderModes()

class PathModes:
    Paths = 0
    Colliders = 1
    Grounds = 2
paths = PathModes()

dev = "--dev" in argv