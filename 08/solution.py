# %%
import re
from collections import defaultdict
from itertools import combinations
# %%
debug = True
in_file = "sample.txt"
in_file = "input.txt"
with open(in_file) as f:
    data = f.read().splitlines()
antennas = defaultdict(list)
for i,row in enumerate(data):
    matches = re.finditer(r"\w", row)
    for match in matches:
        antennas[match.group()].append((i, match.start()))


data = [list(x) for x in data]
n_col = len(data[0])
n_row = len(data)
def show(data):
    print("\n".join(["".join(x) for x in data]))
print(f"{n_row=},{n_col=}")
show(data)
# %%
def get_distance(p1:tuple, p2:tuple):
    return (p1[0]-p2[0], p1[1]-p2[1])

def _get_antinode(p, d):
    return (p[0]+d[0], p[1]+d[1])

def inside_map(p):
    if (p[0]<= n_col-1) and (p[0]>= 0) and (p[1]<= n_row-1) and (p[1]>= 0):
        return True
    return False
    

def get_antinodes(p1:tuple, p2:tuple):
    d = get_distance(p1, p2)
    a1 = _get_antinode(p1, d)
    a2 = _get_antinode(p2, (-d[0],-d[1]))
    out = set()
    if inside_map(a1):
        out.add(a1)
    if inside_map(a2):
        out.add(a2)
    return out

def get_all_antinodes(p1:tuple, d:tuple = None, top_level = True):
    out = set()   
    if inside_map(p1):
        out.update([p1])
    a = _get_antinode(p1,d)
    if top_level:
        d_neg = (-d[0],-d[1])
        b = _get_antinode(p1,d_neg)

    if inside_map(a):
        out.update(get_all_antinodes(a,d, top_level = False))
    if top_level:
        if inside_map(b):
            out.update(get_all_antinodes(b, d_neg,top_level = False))
    return out

    
# %%
part1 = set()
part2 = set()
for ant_type, pos in antennas.items():
    for points in combinations(pos,2):
        current_antinodes = get_antinodes(points[0],points[1])
        part1 = part1.union(current_antinodes)
        d = get_distance(points[0], points[1])
        part2_ant = get_all_antinodes(points[0],d)
        part2 = part2.union(part2_ant)
print(f"part1 = {len(part1)}")
print(f"part2 = {len(part2)}")
