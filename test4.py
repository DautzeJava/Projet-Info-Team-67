import sys  # to change where Python looks for modules
sys.path.append("src")  # add the src folder
import donnees  # loads the JSON files
import game_state  # state of the game
import build  # the new file

config, buildings, monsters, events, highscore = donnees.load_all()  # load data
by_id = {b["id"]: b for b in buildings}  # dict: id -> building data
width = config["map"]["width"]  # map size from config.json
height = config["map"]["height"]
grid = [["." for _ in range(width)] for _ in range(height)]  # empty map
state = game_state.create_state(config)  # new game

ok, msg = build.place_building(state, grid, config, by_id["gold_mine"], 0, 2)
print(ok, msg)
assert ok and state["resources"]["gold"] == 190 and grid[0][2] == "$"  # built and paid 10

ok, msg = build.place_building(state, grid, config, by_id["gold_mine"], 0, 2)
print(ok, msg)
assert not ok  # same cell

ok, msg = build.place_building(state, grid, config, by_id["gold_mine"], 1, 10)
print(ok, msg)
assert not ok  # a mine cannot go in the monster zone

ok, msg = build.place_building(state, grid, config, by_id["trap"], 1, 10)
print(ok, msg)
assert ok and grid[1][10] == "^"  # a trap can

ok, msg = build.place_building(state, grid, config, by_id["trap"], 1, width + 5)
print(ok, msg)
assert not ok  # outside the map

state["resources"]["gold"] = 0  # no money
ok, msg = build.place_building(state, grid, config, by_id["gold_mine"], 2, 2)
print(ok, msg)
assert not ok and grid[2][2] == "."  # refused, nothing placed

print("OK step 4")