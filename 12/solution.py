# %%

import matplotlib.pyplot as plt
import networkx as nx
from shapely import box, union_all

in_file = "sample.txt"
in_file = "sample2.txt"
in_file = "input.txt"
with open(in_file) as f:
    lines = f.read().split()
data = [line.strip() for line in lines]
m, n = len(data), len(data[0])
debug = False
# %%

g = nx.Graph()

# %%
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
for x in range(m):
    for y in range(n):
        pos = (y, x)
        plant = data[y][x]
        g.add_node(pos, plant=plant)
        # check Von Neumann neighborhood
        for dy, dx in directions:
            yn, xn = y + dy, x + dx
            # if valid and same plant type
            if 0 <= yn < m and 0 <= xn < n and data[yn][xn] == plant:
                g.add_edge(pos, (yn, xn), plant=plant)


def cross_product(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]


def get_corners(polygon):
    coords = list(polygon.exterior.coords)  # Get exterior coordinates
    corners = []
    n = len(coords)

    for i in range(n):
        prev_point = coords[(i - 1) % n]
        current_point = coords[i]
        next_point = coords[(i + 1) % n]

        vector1 = (current_point[0] - prev_point[0], current_point[1] - prev_point[1])
        vector2 = (next_point[0] - current_point[0], next_point[1] - current_point[1])

        cross = cross_product(vector1, vector2)

        # If the cross product is non-zero, we have a corner (sharp turn)
        if cross != 0:
            corners.append(current_point)

    return corners


part1 = 0
part2 = 0
for x in nx.components.connected_components(g):
    fe = next(iter(x))
    if debug:
        print(f"plant: {data[fe[0]][fe[1]]}")
        print(x)
    square = [box(point[1], point[0], point[1] + 1, point[0] + 1) for point in x]
    polygon = union_all(square)
    out = polygon.area * polygon.boundary.length
    if debug:
        print(f"area={polygon.area},perimeter={polygon.boundary.length}, price={out}")
    boundary = polygon.boundary.normalize().simplify(0.0)
    if boundary.is_ring:
        part2 += polygon.area * (len(boundary.coords) - 1)
    else:  # some interior elements are there
        for line in boundary.geoms:
            part2 += polygon.area * (len(line.coords) - 1)
    part1 += out
    i, j = polygon.exterior.xy
    if debug:
        plt.plot(i, j, color="blue", linewidth=2)
        plt.show()
        print("\n\n")
print(part1)
print(part2)
# %%
