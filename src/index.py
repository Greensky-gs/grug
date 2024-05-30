from utils.config import configs, renderModes
from p5 import *
from structures.Game import Game
from structures.Loader import Loader

game = Game()  # Crée une instance de la classe Game
loader = Loader()  # Crée une instance de la classe Loader

def setup():
    size(configs["WIDTH"], configs["HEIGHT"])  # Définit la taille de la fenêtre

    game.setup()  # Initialise le jeu
    loader.load()  # Charge les ressources nécessaires

def draw():
    background(0)  # Définit la couleur de fond

    if not loader.ended:  # Si le chargement n'est pas terminé
        loader.display()  # Affiche l'écran de chargement

        if loader.ready and (key_is_pressed or mouse_is_pressed):  # Si le chargement est prêt et une touche ou un bouton de la souris est enfoncé
            loader.end()  # Termine le chargement
        return

    if game.win:  # Si le joueur a gagné
        loader.win()  # Affiche l'écran de victoire
        return
    if not game.ready:  # Si le jeu n'est pas prêt
        return

    if game.player.dead or not game.ready:  # Si le joueur est mort ou le jeu n'est pas prêt
        loader.lostScreen()  # Affiche l'écran de défaite

        if game.tick - game.getcache("endTick", -100) > 3 and (key_is_pressed or mouse_is_pressed) and not game.loading:  # Si le temps écoulé depuis la fin du jeu est supérieur à 3 secondes et une touche ou un bouton de la souris est enfoncé et le jeu n'est pas en cours de chargement
            game.reset()  # Réinitialise le jeu
        return

    # Gère mouvements du joueur
    if key_is_pressed:  # Si une touche est enfoncée
        keysLeft = ["a", "q", "left"]  # Liste des touches pour se déplacer vers la gauche
        keysRight = ["d", "right"]  # Liste des touches pour se déplacer vers la droite
        keysUp = ["z", "up", "w"]  # Liste des touches pour se déplacer vers le haut
        keysDown = ["down", "s"]  # Liste des touches pour se déplacer vers le bas
        combined = keysLeft + keysRight + keysUp + keysDown  # Liste combinée de toutes les touches de déplacement

        pressedKey = str(key).lower()  # Récupère la touche enfoncée en minuscules

        if pressedKey == "backspace":  # Si la touche enfoncée est "backspace"
            pauseTick = game.getcache('pauseTick')  # Récupère le tick de pause depuis le cache
            if pauseTick is None:  # Si le tick de pause n'est pas défini
                game.pause()  # Met le jeu en pause
                return
            else:
                if game.tick - pauseTick >= 1:  # Si le temps écoulé depuis la pause est supérieur ou égal à 1 seconde
                    if game.paused:  # Si le jeu est en pause
                        game.resume()  # Reprend le jeu
                    else:
                        game.pause()  # Met le jeu en pause
                    return

        xMov = 0  # Mouvement horizontal du joueur
        yMov = 0  # Mouvement vertical du joueur
        if pressedKey in combined:  # Si la touche enfoncée fait partie des touches de déplacement
            xMov = 0 if not pressedKey in keysLeft + keysRight else (1 if pressedKey in keysRight else -1)  # Détermine le mouvement horizontal en fonction de la touche enfoncée
            yMov = 0 if not pressedKey in keysUp + keysDown else (-1 if pressedKey in keysUp else 1)  # Détermine le mouvement vertical en fonction de la touche enfoncée

        if not game.paused:  # Si le jeu n'est pas en pause
            game.movePlayer(x=xMov, y=yMov, moving=xMov != 0 or yMov != 0)  # Déplace le joueur
        if game.render == renderModes.FACE:  # Si le mode de rendu est "FACE"
            if pressedKey in keysUp + [" "] and not game.player.jumping:  # Si la touche enfoncée fait partie des touches de saut et le joueur n'est pas en train de sauter
                game.startJump()  # Démarre le saut du joueur
    else:
        if not game.player.jumping:  # Si le joueur n'est pas en train de sauter
            game.grugSprite.setTextureState("idle")  # Définit l'état de texture du personnage principal sur "idle"
            game.player.setTextureState("idle")  # Définit l'état de texture du joueur sur "idle"

    if mouse_is_pressed:  # Si un bouton de la souris est enfoncé
        if game.render == renderModes.FACE and not game.player.jumping:  # Si le mode de rendu est "FACE" et le joueur n'est pas en train de sauter
            game.startJump()  # Démarre le saut du joueur
    game.display()  # Affiche le jeu

run()  # Exécute le jeu
