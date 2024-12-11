# %%
import functools
in_file = "sample.txt"
in_file = "input.txt"
with open(in_file,"r") as f:
    data = f.read().split(" ")
data = [int(x) for x in data]
data
# %%
@functools.lru_cache(None)
def get_stones(stone:int, blink:int=25):
    if blink == 0:
        return 1
    else:
        if stone ==0:
            out = get_stones(1, blink -1)
        elif len(s:=str(stone)) %2 == 0:
            h = len(s) // 2
            out = get_stones(int(s[:h]), blink - 1)
            out += get_stones(int(s[h:]), blink-1)
        else:
            out = get_stones(stone*2024, blink -1)
    return out
# %%
part1 = 0
for x in data:
    part1 += get_stones(x, 25)
print(part1)
# %%
part2 = 0
for x in data:
    part2 += get_stones(x, 75)
print(part2)
# %%
