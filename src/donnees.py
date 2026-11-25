import json

def load_json(path, default=None):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return {} if default is None else default
        return json.loads(content)


def load_all():
    buildings = load_json("data/buildings.json", {})["buildings"]
    config = load_json("data/config.json", {})
    events = load_json("data/events.json", [])
    highscore = load_json("data/highscore.json", [])
    monsters = load_json("data/monsters.json", {})["monsters"]
    return config, buildings, monsters, events, highscore