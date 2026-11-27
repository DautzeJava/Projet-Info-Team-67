def create_state(config):  # build the starting state of a new game
    return {
        "wall_hp": config["wall_hp"],  # current health of the wall
        "resources": dict(config["start_resources"]),  # copy, so config is never changed
        "turn": 1,  # current turn number
        "buildings": [],  # buildings placed by the player
        "monsters": [],  # monsters currently on the map
        "kills": 0,  # normal monsters killed (for the score)
        "boss_kills": 0,  # bosses killed (for the score)
    }

def is_game_over(state):  # the game ends when the wall falls
    return state["wall_hp"] <= 0

def apply_income(state, config, buildings_by_id):  # called at the end of every turn
    for r in state["resources"]:  # basic income (gold, mana, diamonds)
        state["resources"][r] += config["income_per_turn"][r]
    for placed in state["buildings"]:  # then every placed building
        data = buildings_by_id[placed["id"]]  # its data from buildings.json
        for r, amount in data["production"].items():  # what it produces
            state["resources"][r] += amount
        for r, amount in data["consumption"].items():  # what it consumes
            state["resources"][r] -= amount