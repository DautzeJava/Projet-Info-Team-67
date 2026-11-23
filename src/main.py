from donnees import load_config
import map_game
import time


def initialize_game():
    config = load_config("data/config.json")
    print("Texte d'introduction")
    grid = map_game.create_map()
    map_game.display_map(grid)
    return grid


def menu():
    print("Menu des options :")
    options = ["1 : Commencer une partie", "2 : Charger la dernière partie", "3 : Crédits"]
    for option in options:
        print(option)
    compris = int(input("Entrez l'option : "))

    if compris == 1:
        return initialize_game()
    elif compris == 2:
        print("A dev")
        menu()
    elif compris == 3:
        print("eee")
        menu()


grid = menu()