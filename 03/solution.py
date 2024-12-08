# %%
import re
#input_path = "sample.txt"
input_path = "input.txt"
with open(input_path) as f:
    data = f.read()
# %%
pattern = r"mul\(\d+,\d+\)"
x = re.findall(pattern, data)
# %%
s = 0
for match in x:
    m = re.search(r"\d+,\d+",match).group()
    x1,x2 = m.split(",")
    s += int(x1)*int(x2)
s
# %%
#part 2
s = 0
enabled = True
for x1, x2, do, dont in re.findall(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))", data):
    #print(f"{x1=},{x2=},{do=},{dont=}")
    if do or dont:
        enabled = bool(do)
    else:
        s += int(x1)*int(x2)*enabled
s