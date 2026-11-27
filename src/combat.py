def spawn_monster(state, config, data, row, hp_multiplier=1):
    # create a monster at the right edge of the map and add it to the game
    monster = {
        "id": data["id"],  # id from monsters.json
        "name": data["name"],  # display name
        "symbol": data["symbol"],  # symbol shown on the map
        "is_boss": data["is_boss"],  # True for bosses
        "special": data["special"],  # special ability (for example "ignores_traps")
        "hp": int(data["hp"] * hp_multiplier),  # health (stronger in endless waves)
        "displacement": data["displacement"],  # cells moved per turn
        "damage": data["damage"],  # damage dealt to the wall each turn
        "reward": data["reward"],  # resources given when it dies
        "row": row,  # row on the map
        "col": config["map"]["monster_start_column"],  # starts on the right
    }
    state["monsters"].append(monster)  # remember it in the game state
    return monster

def take_damage(monster, damage):  # a monster loses health
    monster["hp"] -= damage

def redraw(state, grid, buildings_by_id):
    # rebuild the whole map from the state: empty cells, then buildings, then monsters
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            grid[r][c] = "."  # empty cell
    for placed in state["buildings"]:  # buildings first
        grid[placed["row"]][placed["col"]] = buildings_by_id[placed["id"]]["symbol"]
    for monster in state["monsters"]:  # monsters on top
        grid[monster["row"]][monster["col"]] = monster["symbol"]

def move_monsters(state, config):
    # every monster advances toward the wall, but stops next to it
    stop_col = config["map"]["wall_column"] + 1  # first column right of the wall
    for monster in state["monsters"]:
        monster["col"] = max(stop_col, monster["col"] - monster["displacement"])

def trigger_traps(state, monster, old_col, buildings_by_id):
    # traps on the cells the monster just walked over hit it, then disappear
    if monster["special"] == "ignores_traps":  # elves ignore traps
        return
    used = []  # traps that were triggered
    for col in range(old_col - 1, monster["col"] - 1, -1):  # cells passed, right to left
        for placed in state["buildings"]:
            data = buildings_by_id[placed["id"]]
            if data["type"] == "trap" and placed["row"] == monster["row"] and placed["col"] == col:
                take_damage(monster, data["damage"])  # the trap hits
                used.append(placed)
    for placed in used:  # a trap works only once
        state["buildings"].remove(placed)

def towers_shoot(state, buildings_by_id):
    # every defense building shoots the closest monster inside its range
    for placed in state["buildings"]:
        data = buildings_by_id[placed["id"]]
        if data["type"] != "defense":  # only towers shoot
            continue
        target = None  # the monster we will shoot
        best = None  # its distance
        for monster in state["monsters"]:
            if monster["hp"] <= 0:  # already dead
                continue
            distance = abs(monster["row"] - placed["row"]) + abs(monster["col"] - placed["col"])
            if distance <= data["range"] and (best is None or distance < best):
                target = monster
                best = distance
        if target is not None:
            take_damage(target, data["damage"])

def monsters_attack_wall(state, config):
    # monsters standing next to the wall hit it; returns the total damage dealt
    stop_col = config["map"]["wall_column"] + 1
    total = 0
    for monster in state["monsters"]:
        if monster["col"] == stop_col:  # it reached the wall
            total += monster["damage"]
    state["wall_hp"] -= total  # the wall loses health
    return total

def collect_dead(state):
    # remove dead monsters, give their rewards and count the kills
    alive = []  # monsters that survive
    for monster in state["monsters"]:
        if monster["hp"] <= 0:  # dead
            for r, amount in monster["reward"].items():
                state["resources"][r] += amount  # reward
            if monster["is_boss"]:
                state["boss_kills"] += 1  # a boss was killed
            else:
                state["kills"] += 1  # a normal monster was killed
        else:
            alive.append(monster)
    state["monsters"] = alive  # keep only the living ones

def monsters_turn(state, grid, config, buildings_by_id):
    # one full turn: move, traps, towers shoot, remove the dead, wall attack, redraw
    old_cols = [m["col"] for m in state["monsters"]]  # positions before moving
    move_monsters(state, config)
    for monster, old_col in zip(state["monsters"], old_cols):
        trigger_traps(state, monster, old_col, buildings_by_id)
    towers_shoot(state, buildings_by_id)
    collect_dead(state)  # dead monsters do not attack
    damage = monsters_attack_wall(state, config)
    redraw(state, grid, buildings_by_id)
    return damage