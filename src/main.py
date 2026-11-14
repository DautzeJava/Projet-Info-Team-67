from donnees import charger_config
import map

def initilize_game():
    config = charger_config("")

    map_game = create_map(
        config["map_lenght"]
        config["map_width"]
    )