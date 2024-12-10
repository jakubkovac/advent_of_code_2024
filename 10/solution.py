# %%
import numpy as np
in_file = "sample.txt"
in_file = "input.txt"
with open(in_file) as f:
    data = f.read().splitlines()
data = [[int(y) for y in x] for x in data]
data = np.array(data)
data
data = np.pad(data,pad_width = 1, constant_values=-2, mode = "constant")
# %%
spr, spc = np.where(data == 0) 
starting_points = list(zip(spr, spc))

# %%
def get_flanders(here:tuple) -> list[tuple[int, int]]:
    moves = [(here[0], here[1] +1),(here[0], here[1] -1),(here[0] +1,here[1]),(here[0]-1,here[1])]
    keys = ["right","left","down","up"]
    return keys, moves

def check_around(data:np.ndarray, here:tuple, current_value:int |None =0):
    if current_value is None:
        current_value = data[here]
    keys, moves = get_flanders(here)
    end_coords = []
    for key, move in zip(keys, moves):
        if data[move] -1 == current_value:
            if current_value == 8:
                end_coords.append(move)
            else:
                end_coords.extend(check_around(data, move, current_value + 1))
    return end_coords
# %%
part1 = 0
part2 = 0
for sp in starting_points:
    p  = check_around(data, sp, 0)
    n = len(set(p))
    print(f"{sp=},{n=}")
    part1 += n
    part2 += len(p)
print(part1)
print(part2)
# %%
