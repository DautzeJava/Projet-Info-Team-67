import json


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all():
    buildings = load_json("data/buildings.json")["buildings"]
    config = load_json("data/config.json")
    events = load_json("data/events.json")
    highscore = load_json("data/highscore.json")
    monsters = load_json("data/monsters.json")["monsters"]
    return config, buildings, monsters, events, highscore