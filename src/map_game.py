def create_map(map_lenght, map_width):
    grid = []
    for i in range(map_lenght):
        line = []
        for j in range(map_width):
            line.append("X")
        grid.append(line)
    return grid

def display_map(grid):
    nb_cols = len(grid[0])

    header = "   " + " ".join(f"{c:2d}" for c in range(nb_cols))
    print(header)

    for idx, line in enumerate(grid):
        print(f"{idx:2d}  " + "  ".join(line))