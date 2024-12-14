# %%
import re

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import label

# in_file = "sample.txt"
# m, n = (7, 11)
in_file = "input.txt"
m, n = (103, 101)
board = np.zeros((m, n), dtype=int)
with open(in_file) as f:
    d = f.read().splitlines()
robots = []
for line in d:
    li = list(map(int, re.findall(r"-?\d+", line)))
    # switch positions because of how matrix is indexed
    robots.append({"pos": (li[1], li[0]), "vel": (li[3], li[2])})
robots


# %%
def update_board(robots):
    board = np.zeros((m, n), dtype=int)
    for robot in robots:
        board[robot["pos"]] += 1
    return board


b = update_board(robots)
print(b)


def print_board(board):
    for x in board:
        print("".join([str(y).replace("0", ".") for y in x]))


def update_robots(robots, m, n, seconds=1):
    out = []
    for robot in robots:
        px = (robot["pos"][0] + seconds * robot["vel"][0]) % m
        py = (robot["pos"][1] + seconds * robot["vel"][1]) % n
        out.append({"pos": (px, py), "vel": robot["vel"]})
    return out


def quick_sum(board):
    return int(sum(sum(board)))


def get_quadrants(board):
    m, n = board.shape
    mid_row = m // 2
    mid_col = n // 2
    q1 = board[:mid_row, :mid_col]  # Top-left
    q2 = board[:mid_row, mid_col + 1 :]  # Top-right
    q3 = board[mid_row + 1 :, :mid_col]  # Bottom-left
    q4 = board[mid_row + 1 :, mid_col + 1 :]  # Bottom-right
    return quick_sum(q1) * quick_sum(q2) * quick_sum(q3) * quick_sum(q4)


# %%
for i in range(5):
    print_board(update_board(update_robots([robots[10]], m, n, i)))
    print("\n")
# %%
bb = update_board(update_robots(robots, m, n, 100))
print_board(bb)
get_quadrants(bb)

# %%
bs = []
structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
for i in range(10000):
    # print(f"Iteration={i} ------------------------------------------------")
    bb = update_board(update_robots(robots, m, n, i))
    labeled, num_features = label(bb != 0, structure=structure)
    # Compute the size of each labeled region
    blob_sizes = np.bincount(labeled.ravel())[1:]  # Skip the background (label 0)
    largest_blob_size = blob_sizes.max() if blob_sizes.size > 0 else 0
    bs.append(largest_blob_size)

look_here = np.where(bs == max(bs))[0][0]
look_here
# %%
for i in list(range(look_here - 5, look_here + 5)):
    bb = update_board(update_robots(robots, m, n, i))
    plt.imshow(bb, cmap="viridis")
    plt.title(i)
    plt.show()

# %%
