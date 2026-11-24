def spawn_monster(monster_data, map_size):
    monster = monster_data.copy()
    monster["position"] = map_size - 1
    return monster


def move_monster(monster):
    monster["position"] -= monster["displacement"]


def take_damage(monster, damage):
    monster["hp"] -= damage


def is_dead(monster):
    return monster["hp"] <= 0


def attack_wall(monster):
    return monster["damage"]