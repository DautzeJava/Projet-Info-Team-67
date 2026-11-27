import sys  # to change where Python looks for modules
sys.path.append("src")  # add the src folder
import donnees  # loads the JSON files
import game_state  # the new file

config, buildings, monsters, events, highscore = donnees.load_all()  # load data
buildings_by_id = {b["id"]: b for b in buildings}  # dict: id -> building data

state = game_state.create_state(config)  # new game
print("start:", state["wall_hp"], state["resources"], "turn", state["turn"])
assert state["wall_hp"] == 300  # wall starts at 300
assert state["resources"] == {"gold": 200, "mana": 50, "diamonds": 5}

state["buildings"].append({"id": "gold_mine"})  # pretend we built a gold mine
game_state.apply_income(state, config, buildings_by_id)  # end of turn
print("after income:", state["resources"])
assert state["resources"]["gold"] == 210  # 200 + 5 (basic) + 5 (mine)
assert state["resources"]["mana"] == 52  # 50 + 2 (basic)
assert config["start_resources"]["gold"] == 200  # config was NOT changed

assert game_state.is_game_over(state) is False  # wall still standing
state["wall_hp"] = 0  # destroy the wall
assert game_state.is_game_over(state) is True  # now the game is over
print("OK step 3")