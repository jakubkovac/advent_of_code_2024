
# %%
import numpy as np
from copy import deepcopy
from collections import defaultdict

in_file = "sample.txt"
in_file = "input.txt"
with open(in_file) as f:
    data = f.read().splitlines()
data = [list(line.strip()) for line in data]
input_data = np.array(data)
data = deepcopy(input_data)
# %%
direction_map = {
"up": [0,-1],
"right": [1,0],
"down" : [0,1],
"left" : [-1,0]
}

dir_keys = list(direction_map.keys())

def next_step(x,y,direction) -> tuple:
    dir = direction_map[direction]
    return(x+dir[0], y+dir[1])

def is_outside(x,y,m,n):
    if x<0 or y<0 or x>=m or y>=n:
        return True
    return False

def is_blocked(data, x, y):
    if data[y,x]=="#" or data[y,x] =="O":
        return True
    return False

def turn_right(direction):
    now = int(np.where([x == direction for x in  dir_keys])[0][0])
    return dir_keys[(now + 1)%4]

def add_path(direction) ->str:
    if direction in ["up","down"]:
        return "|"
    return "-"
# %%

n,m = data.shape
pos_y,pos_x = np.where(data == "^")
pos_x = int(pos_x[0])
pos_y = int(pos_y[0])
direction = "up"
outside = False
i = 0
print(f"Starting here: {pos_x=},{pos_y=},{direction=}")
while (not outside):
    i += 1
    n_pos_x, n_pos_y = next_step(pos_x, pos_y, direction)
    outside = is_outside(n_pos_x, n_pos_y,m,n)
    if not outside:
        if is_blocked(data, n_pos_x, n_pos_y):
            direction = turn_right(direction)
        else:
            pos_x, pos_y = n_pos_x, n_pos_y
            data[pos_y,pos_x] = "X"
        outside = is_outside(pos_x, pos_y,m,n)

ans = int(sum(sum(data == "X"))) + int(sum(sum(data == "^")))
print(ans)
# %%

possibilities = 0
it = 0
max_it = m*n
for row in range(m):
    for col in range(n):
        it += 1
        if it % 1000 == 0:
            print(f"{it}/{max_it}")
        data = deepcopy(input_data)
        visited = defaultdict(lambda: defaultdict(list))
        if data[row,col] == ".":
            data[row,col] = "O"
            outside = False
            loop = False
            direction = "up"
            pos_y,pos_x = np.where(data == "^")
            pos_x = int(pos_x[0])
            pos_y = int(pos_y[0])
            old_direction = direction
            i = 0
            while (not outside) or loop:
                i +=1
                n_pos_x, n_pos_y = next_step(pos_x, pos_y, direction)
                outside = is_outside(n_pos_x, n_pos_y,m,n)
                if not outside:
                    if is_blocked(data, n_pos_x, n_pos_y):
                        old_direction = direction
                        direction = turn_right(direction)
                        data[pos_y,pos_x] = "+"
                    else:
                        pos_x, pos_y = n_pos_x, n_pos_y
                        new_sign = add_path(direction)
                        old_sign = data[pos_y,pos_x]
                        if old_sign == new_sign:
                            if direction in visited[pos_y][pos_x]:
                                loop =True
                                break
                            else:
                                visited[pos_y][pos_x].append(direction)
                        if data[pos_y,pos_x] == "^":
                            pass
                        elif (new_sign == "|" and old_sign == "-") or (new_sign == "-" and old_sign == "|"):
                            data[pos_y,pos_x] = "+"
                        else:
                            data[pos_y,pos_x] = new_sign
                    outside = is_outside(pos_x, pos_y,m,n)
            possibilities += loop
print(f"{possibilities=}")