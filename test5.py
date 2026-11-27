import sys  # to change where Python looks for modules
sys.path.append("src")  # add the src folder
import donnees  # loads the JSON files
import game_state  # state of the game
import build  # building rules
import combat  # monsters, traps and towers

config, buildings, monsters, events, highscore = donnees.load_all()  # load data
b_by_id = {b["id"]: b for b in buildings}  # id -> building data
m_by_id = {m["id"]: m for m in monsters}  # id -> monster data

def new_game():  # a fresh state and an empty map for every test
    grid = [["." for _ in range(config["map"]["width"])] for _ in range(config["map"]["height"])]
    return game_state.create_state(config), grid

# --- Test A: a trap kills a goblin that walks over it ---
state, grid = new_game()
ok, msg = build.place_building(state, grid, config, b_by_id["trap"], 3, 15)
assert ok, msg  # the trap must be built
goblin = combat.spawn_monster(state, config, m_by_id["goblin"], 3)  # hp 20, moves 2
combat.monsters_turn(state, grid, config, b_by_id)  # 19 -> 17
assert goblin["hp"] == 20 and len(state["buildings"]) == 1  # nothing happened yet
combat.monsters_turn(state, grid, config, b_by_id)  # 17 -> 15, walks over the trap
print("A: kills", state["kills"], "| traps left", len(state["buildings"]))
assert state["kills"] == 1 and state["monsters"] == []  # the trap (20 damage) killed it
assert state["buildings"] == [] and grid[3][15] == "."  # the trap was used up

# --- Test B: an elf ignores traps ---
state, grid = new_game()
build.place_building(state, grid, config, b_by_id["trap"], 4, 18)
elf = combat.spawn_monster(state, config, m_by_id["elf"], 4)  # hp 40, moves 1
combat.monsters_turn(state, grid, config, b_by_id)  # 19 -> 18, on the trap
print("B: elf hp", elf["hp"], "| traps left", len(state["buildings"]))
assert elf["hp"] == 40 and len(state["buildings"]) == 1  # not hurt, trap still there

# --- Test C: an archer tower shoots only when the monster is in range ---
state, grid = new_game()
ok, msg = build.place_building(state, grid, config, b_by_id["archer_tower"], 5, 9)
assert ok, msg
orc = combat.spawn_monster(state, config, m_by_id["orc"], 5)  # hp 80, moves 1
for turn in range(1, 5):  # turns 1-4: the orc is at columns 18..15, too far
    combat.monsters_turn(state, grid, config, b_by_id)
assert orc["hp"] == 80  # range is 5, distance is still 6 or more
combat.monsters_turn(state, grid, config, b_by_id)  # turn 5: orc at column 14, distance 5
print("C: orc hp", orc["hp"], "at column", orc["col"])
assert orc["col"] == 14 and orc["hp"] == 72  # archer damage is 8

print("OK step 6")