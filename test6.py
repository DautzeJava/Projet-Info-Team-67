import sys  # to change where Python looks for modules
sys.path.append("src")  # add the src folder
import donnees  # loads the JSON files
import game_state  # state of the game
import build  # building rules
import combat  # monsters, traps and towers
import turns  # the new file

config, buildings, monsters, events, highscore = donnees.load_all()  # load data
b_by_id = {b["id"]: b for b in buildings}  # id -> building data
m_by_id = {m["id"]: m for m in monsters}  # id -> monster data

class FakeRng:  # a "random" generator we control, so the test gives the same result every time
    def __init__(self, value):
        self.value = value  # what random() returns
    def random(self):
        return self.value  # 0.0 = every event happens, 0.99 = none happens
    def randint(self, a, b):
        return a  # always the first row
    def choice(self, seq):
        return seq[0]  # always the first item

def new_game():  # a fresh state and an empty map
    grid = [["." for _ in range(config["map"]["width"])] for _ in range(config["map"]["height"])]
    return game_state.create_state(config), grid

start_col = config["map"]["monster_start_column"]

# --- Test A: a scheduled wave (turn 3 = 3 goblins) ---
state, grid = new_game()
turns.spawn_wave(state, config, events, m_by_id, 3, FakeRng(0.99))
print("A:", [m["id"] for m in state["monsters"]])
assert [m["id"] for m in state["monsters"]] == ["goblin"] * 3

# --- Test B: an endless wave (turn 55 = wave number 2) ---
state, grid = new_game()
e = events["endless_waves"]
turn = e["start_turn"] + e["interval"]  # the second endless wave
turns.spawn_wave(state, config, events, m_by_id, turn, FakeRng(0.99))
expected_count = e["base_count"] + e["extra_monster_per_wave"]  # wave 2 has one extra monster
expected_hp = int(m_by_id["goblin"]["hp"] * e["hp_multiplier_per_wave"] ** 2)  # stronger goblins
print("B:", len(state["monsters"]), "monsters, goblin hp", state["monsters"][0]["hp"])
assert len(state["monsters"]) == expected_count
assert state["monsters"][0]["hp"] == expected_hp
turns.spawn_wave(state, config, events, m_by_id, turn + 1, FakeRng(0.99))  # a turn between waves
assert len(state["monsters"]) == expected_count  # nothing new appeared

# --- Test C: random events ---
state, grid = new_game()
turns.apply_random_events(state, events, FakeRng(0.0))  # every event happens
print("C:", state["resources"], "wall", state["wall_hp"])
assert state["resources"] == {"gold": 210, "mana": 80, "diamonds": 6}  # +50 -40 gold, +30 mana, +1 diamond
assert state["wall_hp"] == 260  # the earthquake did 40
state, grid = new_game()
assert turns.apply_random_events(state, events, FakeRng(0.99)) == []  # nothing happened
assert state["resources"]["gold"] == 200
state, grid = new_game()
state["resources"]["gold"] = 10
only_plague = {"random_events": [ev for ev in events["random_events"] if ev["id"] == "plague"]}
turns.apply_random_events(state, only_plague, FakeRng(0.0))
assert state["resources"]["gold"] == 0  # resources never go below zero

# --- Test D: three full turns ---
state, grid = new_game()
build.place_building(state, grid, config, b_by_id["gold_mine"], 0, 2)  # +5 gold per turn
rng = FakeRng(0.99)
turns.play_turn(state, grid, config, events, b_by_id, m_by_id, rng)  # turn 1
turns.play_turn(state, grid, config, events, b_by_id, m_by_id, rng)  # turn 2
assert state["turn"] == 3 and state["monsters"] == []  # no wave yet
assert state["resources"]["gold"] == 190 + 2 * 10  # 190 after building + 2 turns x (5 basic + 5 mine)
turns.play_turn(state, grid, config, events, b_by_id, m_by_id, rng)  # turn 3: the wave appears
print("D: turn", state["turn"], "monsters", len(state["monsters"]))
assert state["turn"] == 4 and len(state["monsters"]) == 3
assert all(m["col"] == start_col for m in state["monsters"])  # waiting at the right edge
assert grid[0][start_col] == "g"  # visible on the map
turns.play_turn(state, grid, config, events, b_by_id, m_by_id, rng)  # turn 4: they advance
assert all(m["col"] == start_col - 2 for m in state["monsters"])

# --- Test E: the wall falls ---
state, grid = new_game()
state["wall_hp"] = 3
g = combat.spawn_monster(state, config, m_by_id["goblin"], 0)
g["col"] = config["map"]["wall_column"] + 1  # already next to the wall
turns.play_turn(state, grid, config, events, b_by_id, m_by_id, FakeRng(0.99))
print("E: wall hp", state["wall_hp"])
assert game_state.is_game_over(state) and state["turn"] == 1  # the game stops, no new turn

# --- Test F: the score ---
state, grid = new_game()
state["turn"], state["kills"], state["boss_kills"] = 11, 4, 1  # 10 turns survived
print("F: score", turns.compute_score(state, config))
assert turns.compute_score(state, config) == 10 * 10 + 4 * 5 + 1 * 50

print("OK step 7")