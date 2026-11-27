def zone_of(column, config):  # which zone a column belongs to
    if column <= config["map"]["village_last_column"]:  # left side of the map
        return "village"
    if column == config["map"]["wall_column"]:  # the wall column
        return "wall_column"
    return "monster_zone"  # everything to the right of the wall

def count_built(state, building_id):  # how many of this building already exist
    total = 0
    for placed in state["buildings"]:
        if placed["id"] == building_id:
            total += 1
    return total

def place_building(state, grid, config, data, row, col):
    # returns (True, message) if built, or (False, reason) if refused
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return False, "Position outside the map."  # row/col must exist on the map
    if zone_of(col, config) != data["zone"]:
        return False, "This building must be placed in: " + data["zone"] + "."
    if grid[row][col] != ".":
        return False, "This cell is already used."
    if count_built(state, data["id"]) >= data["max_count"]:
        return False, "You reached the maximum number of " + data["name"] + "."
    if state["resources"]["gold"] < data["price"]:
        return False, "Not enough gold."
    state["resources"]["gold"] -= data["price"]  # pay
    state["buildings"].append(
        {"id": data["id"], "level": 1, "hp": data["hp"], "row": row, "col": col}
    )  # remember the building (with its position)
    grid[row][col] = data["symbol"]  # show it on the map
    return True, data["name"] + " built."