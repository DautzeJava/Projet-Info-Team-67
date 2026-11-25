import donnees
import map_game
import os
import time
import menu


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def initialize_game():
    config, buildings, monsters, events, highscore = donnees.load_all()
    grid = map_game.create_map()
    map_game.display_map(grid)
    return grid


def main():
    while True:
        clear()
        choix = menu.menu_init()

        if choix == 1:
            clear()
            return initialize_game()
        elif choix == 2:
            print("\nA dev")
            time.sleep(1.5)
        elif choix == 3:
            print("\nEquipe 67 : Félix Pastor et David Stefan Raducan")
            input("\nAppuyez sur Entrée pour revenir au menu...")
        elif choix == 4:
            clear()
            exit()


main()