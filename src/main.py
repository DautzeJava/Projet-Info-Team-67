from donnees import load_config
import map_game
import time


def initialize_game():
    config = load_config("data/config.json")

    grid = map_game.create_map()
    map_game.display_map(grid)
    return grid

grid = initialize_game()


time.sleep(2)

map_game.update_map(grid, 2, 3, 'A')