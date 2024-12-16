# %%
import heapq

import numpy as np

in_file = "sample.txt"
in_file = "input.txt"
with open(in_file) as f:
    data = f.read().split()
data = np.array([list(line) for line in data])
data
# %%
pos = np.where(data == "S")
sy, sx = (pos[0][0], pos[1][0])
pos = np.where(data == "E")
ey, ex = (pos[0][0], pos[1][0])

moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]


# %%
def dijkstra(data, sx, sy, ex, ey):
    # starting with 0 cost at sx, sy
    # facing east, only with the initial node in my set
    q = [(0, sx, sy, 1, 0, {(sx, sy)})]
    seen = set()

    while len(q) > 0:
        # extract node with the lowest cost
        d, x, y, dx, dy, path = heapq.heappop(q)

        if (x, y) in seen:
            continue
        seen.add((x, y))
        if (x, y) == (ex, ey):
            return d, path

        for mx, my in moves:
            if mx == -dx and my == -dy:
                # skip the reverse of previous moves
                continue
            new_x, new_y = x + mx, y + my
            is_straight = abs(mx) == abs(dx) and abs(my) == abs(dy)
            cost = 1
            if not is_straight:
                cost += 1000
            else:
                cost = 1
            if data[new_y][new_x] == "#" or (new_x, new_y) in seen:
                # skip visited/walls
                continue
            new_path = path.copy()
            new_path.add((new_x, new_y))
            heapq.heappush(q, (d + cost, new_x, new_y, mx, my, new_path))
    return None, None


# %%
score, path = dijkstra(data, sx, sy, ex, ey)
print(score)

# %%
possible_seats = set()
possible_seats.update(path)
for px, py in path:
    if (px, py) == (ex, ey) or (px, py) == (sx, sy):
        continue

    data[py][px] = "#"
    cost, p = dijkstra(data, sx, sy, ex, ey)
    if cost == score:
        possible_seats.update(p)
    data[py][px] = "."

print(len(possible_seats))

# %%
