import random  # for random rows and random events
import combat  # monsters, traps and towers
import game_state  # state of the game

def spawn_monsters_of_wave(state, config, m_by_id, monster_ids, rng, hp_multiplier=1):
    # create one monster for every id in the list, each on a random row
    for monster_id in monster_ids:
        row = rng.randint(0, config["map"]["height"] - 1)  # random row
        combat.spawn_monster(state, config, m_by_id[monster_id], row, hp_multiplier)

def spawn_wave(state, config, events, m_by_id, turn, rng=random):
    # create the monsters that must appear on this turn (scheduled + endless waves)
    for wave in events["waves"]:  # scheduled waves
        if wave["turn"] == turn:
            ids = []
            for monster_id, count in wave["monsters"].items():
                ids += [monster_id] * count  # "goblin": 3 -> goblin, goblin, goblin
            spawn_monsters_of_wave(state, config, m_by_id, ids, rng)
    endless = events["endless_waves"]  # waves that never end
    if turn >= endless["start_turn"] and (turn - endless["start_turn"]) % endless["interval"] == 0:
        number = (turn - endless["start_turn"]) // endless["interval"] + 1  # 1, 2, 3...
        count = endless["base_count"] + endless["extra_monster_per_wave"] * (number - 1)
        multiplier = endless["hp_multiplier_per_wave"] ** number  # monsters get stronger
        ids = [rng.choice(endless["monster_pool"]) for _ in range(count)]  # random monsters
        if number % endless["boss_every_n_waves"] == 0:  # every n waves a boss comes too
            boss_index = (number // endless["boss_every_n_waves"] - 1) % len(endless["boss_pool"])
            ids.append(endless["boss_pool"][boss_index])
        spawn_monsters_of_wave(state, config, m_by_id, ids, rng, multiplier)

def apply_random_events(state, events, rng=random):
    # each random event happens with its own probability; returns the messages to show
    messages = []
    for ev in events["random_events"]:
        if rng.random() < ev["probability"]:  # did it happen?
            if ev["type"] == "gain":
                state["resources"][ev["resource"]] += ev["amount"]
            elif ev["type"] == "loss":  # never go below zero
                state["resources"][ev["resource"]] = max(0, state["resources"][ev["resource"]] - ev["amount"])
            elif ev["type"] == "damage_wall":
                state["wall_hp"] -= ev["amount"]
            messages.append(ev["name"] + ": " + ev["description"])
    return messages

def compute_score(state, config):
    # score = turns survived, monsters killed and bosses killed (values from config.json)
    s = config["score"]
    turns_survived = state["turn"] - 1  # turn 1 means nothing survived yet
    return (turns_survived * s["per_turn_survived"]
            + state["kills"] * s["per_monster_killed"]
            + state["boss_kills"] * s["per_boss_killed"])

def play_turn(state, grid, config, events, b_by_id, m_by_id, rng=random):
    # everything that happens after the player ends the turn; returns the messages
    messages = apply_random_events(state, events, rng)  # 1. random events
    combat.monsters_turn(state, grid, config, b_by_id)  # 2. monsters move, traps, towers, wall
    if game_state.is_game_over(state):  # the wall fell: stop here
        return messages
    spawn_wave(state, config, events, m_by_id, state["turn"], rng)  # 3. new monsters appear
    game_state.apply_income(state, config, b_by_id)  # 4. resources
    combat.redraw(state, grid, b_by_id)  # 5. update the map
    state["turn"] += 1  # 6. next turn
    return messages