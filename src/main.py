import donnees
import map_game
import os
import menu


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def initialize_game():
    config, buildings, monsters, events, highscore = donnees.load_all()
    grid = map_game.create_map()
    map_game.display_map(grid)
    game_running = True
    return game_running, grid


def main():

    print("Il était une fois dans une contrée lointaine")
    input("Entrez quelque chose pour continuer :")
    game_running = False
    while True:
        clear()
        game_running, grid = menu.menu_init(initialize_game, clear, game_running)
        while game_running:
            clear()
            map_game.display_map(grid)
            menu.menu_in_game(game_running, clear)


main()