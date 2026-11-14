from donnees import load_config
import map_game

def initialize_game():
    config = load_config("data/config.json")

    grid = map_game.create_map(
        config["Map_lenght"],
        config["Map_width"]
    )
    map_game.display_map(grid)
    return grid

if __name__ == "__main__":
    initialize_game()