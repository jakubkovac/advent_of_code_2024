# %%
import copy

import numpy as np

in_file = "sample3.txt"
# in_file = "sample2.txt"
# in_file = "input.txt"
with open(in_file) as f:
    data = f.read().split("\n\n")
board = data[0].splitlines()
board2 = copy.deepcopy(board)
moves = list(data[1].replace("\n", ""))
board = np.array([list(line) for line in board])
m, n = board.shape
board2 = [
    x.replace("#", "##").replace(".", "..").replace("O", "[]").replace("@", "@.")
    for x in board2
]
board2 = np.array([list(line) for line in board2])
m2, n2 = board2.shape


def print_board(board):
    for row in board:
        print("".join(row))


print_board(board)
print_board(board2)


# %%
def get_current_position(board):
    out = np.where(board == "@")
    return (out[0][0], out[1][0])


move_map = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


def element_plus(x: tuple, y: tuple):
    return (x[0] + y[0], x[1] + y[1])


def element_minus(x: tuple, y: tuple):
    return (x[0] - y[0], x[1] - y[1])


def look_some_more(board, start, direction):
    rows, cols = board.shape
    r, c = start
    dr, dc = direction

    indices = []

    # Traverse in the direction while staying within bounds
    while 0 <= r < rows and 0 <= c < cols:
        if board[r, c] not in ["O", "[", "]"]:
            if board[r, c] == ".":
                indices.append((r, c))  # Include the '.' in the result
                return indices
            return None  # Return an empty list if it's not '.'
        # Add the current "O" index to the list
        indices.append((r, c))
        # Move in the direction
        r += dr
        c += dc

    return None


def sort_boxes(boxes):
    return sorted(boxes, key=lambda coord: (coord[0], coord[1]))


# %%
box_signs = ["[", "]"]


def move_once(board, move, c_pos: tuple | None = None):
    print(f"move {move}")
    if c_pos is None:
        c_pos = get_current_position(board)
    move_direction = move_map[move]
    next_pos = element_plus(c_pos, move_direction)
    if board[next_pos] == "#":
        return board
    if board[next_pos] == ".":
        board[next_pos] = "@"
        board[c_pos] = "."
        return board
    if board[next_pos] in ["O"] + box_signs:
        if board[next_pos] == "O" or move in ["<", ">"]:
            all_updates = look_some_more(board, next_pos, move_direction)

            if all_updates is None:
                return board
            all_updates = sort_boxes(all_updates[1:])
            rows, cols = zip(*all_updates)
            if board[next_pos] == "O":
                board[rows, cols] = "O"
            else:
                board[rows, cols] = [
                    "[" if i % 2 == 0 else "]" for i in range(len(rows))
                ]
            board[next_pos] = "@"
            board[c_pos] = "."
            return board
        else:
            my_box = get_full_box(board, next_pos)
            all_connected_boxes = boxes_pushing_aswell(board, my_box, move_direction)
            if (-1, -1) in all_connected_boxes:
                return board
            all_connected_boxes = sort_boxes(all_connected_boxes)
            if move == "v":
                all_connected_boxes = list(reversed(all_connected_boxes))
            print(all_connected_boxes)
            for box in all_connected_boxes:
                # change one above/below to this
                below = element_minus(box, move_direction)
                if below[0] == c_pos[0]:
                    if below[1] == c_pos[1]:
                        board[box] = "@"
                    else:
                        board[box] = "."
                else:
                    board[box] = board[below]
            board[next_pos] = "@"
            board[c_pos] = "."
            # set the other one to "."
            return board


def get_full_box(board, pos):
    if board[pos] == "[":
        return [pos, element_plus(pos, (0, 1))]
    if board[pos] == "]":
        return [element_plus(pos, (0, -1)), pos]


def boxes_pushing_aswell(board, box: list[tuple], direction):
    # left_side:
    out = []
    left_side = element_plus(box[0], direction)
    right_side = element_plus(box[1], direction)
    if board[left_side] == "#" or board[right_side] == "#":
        return [(-1, -1)]
    else:
        out.append(box[0])
        out.append(box[1])
        if board[left_side] in box_signs:
            out.append(left_side)
            out.extend(
                boxes_pushing_aswell(board, get_full_box(board, left_side), direction)
            )
        if board[left_side] == ".":
            out.append(left_side)
        if board[right_side] == ".":
            out.append(right_side)
        if board[right_side] in box_signs:
            out.append(right_side)
            out.extend(
                boxes_pushing_aswell(board, get_full_box(board, right_side), direction)
            )
    return list(set(out))


def part1(board):
    coords = np.where(b == "O")
    return sum(100 * coords[0]) + sum(coords[1])


def part2(board):
    coords = np.where(b == "[")
    return sum(100 * coords[0]) + sum(coords[1])


# %%
b = board
for m in moves:
    b = move_once(b, m)
    print_board(b)
    print("\n")

part1(b)
# %%
b = board2
print_board(board2)
print("\n")
for i, m in enumerate(moves):
    b = move_once(b, m)
    if i > 280 and i < 320:
        if i == 308:
            debu = copy.deepcopy(b)
        print(f"Iteration: {i}")
        print_board(b)
        print("\n")
print_board(b)


part2(b)

# %%
print_board(debu)
move_once(debu, "v")
