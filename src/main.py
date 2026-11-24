from donnees import load__all
import map_game
import time
import os


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def initialize_game():
    config, buildings, monsters, events, highscore = donnees.load__all()
    print("Texte d'introduction")
    grid = map_game.create_map()
    map_game.display_map(grid)
    return grid




def menu_init():
    while True:
        clear()
        print("Menu des options :")
        options = [
            "1 : Commencer une partie",
            "2 : Charger la dernière partie",
            "3 : Crédits",
            "4 : Quitter le jeu",
        ]
        for option in options:
            print(option)

        try:
            compris = int(input("Entrez l'option choisie : "))
        except ValueError:
            print("\nVeuillez entrer un chiffre valide (1 à 4).")
            time.sleep(1.2)
            continue

        print("\n")

        if compris == 1:
            clear()
            return initialize_game()
        elif compris == 2:
            print("A dev\n")
            time.sleep(1.5)
        elif compris == 3:
            print("Equipe 67 : Félix Pastor et David Stefan Raducan\n")
            input("Appuyez sur Entrée pour revenir au menu...")
        elif compris == 4:
            clear()
            exit()
        else:
            print("Option invalide : choisissez entre 1 et 4.\n")
            time.sleep(1)

def main():
    grid = menu_init()


main()