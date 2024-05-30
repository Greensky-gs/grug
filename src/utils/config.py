from sys import argv

# Configuration des paramètres
configs = {
    "WIDTH": 1500,  # Largeur de l'écran
    "HEIGHT": 900,  # Hauteur de l'écran
    "loadingTime": 200  # Temps de chargement en millisecondes
}

# Classe pour les modes de rendu
class RenderModes:
    UP = "up",  # Mode de rendu vers le haut
    FACE = "face"  # Mode de rendu vers le visage

renderModes = RenderModes()

# Classe pour les modes de chemin
class PathModes:
    Paths = 0  # Mode pour les chemins
    Colliders = 1  # Mode pour les collisions
    Grounds = 2  # Mode pour les terrains

paths = PathModes()

# Vérification du mode développeur
dev = "--dev" in argv