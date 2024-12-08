# %%
import numpy as np
import re
# %%
with open("input.txt","r") as f:
    out =f.read().splitlines()
data = np.array([list(x) for x in out])
data2 = np.fliplr(data)
n = data.shape[0]
# %%
def find_xmas(s):
    return len(re.findall(pattern="XMAS",string =s)) + len(re.findall(pattern="SAMX",string =s))

def ez_find(m):
    return find_xmas("".join(m))
# %%
n_xmas = 0
for i in range(n):
    col = data[:,i]
    line = data[i,:]
    lower_diag = np.diagonal(data, offset = i)
    lower_diag_f = np.diagonal(data2, offset = i)
    if i != 0:
        upper_diag = np.diagonal(data, offset = -i)
        upper_diag_f = np.diagonal(data2, offset = -i)
        n_xmas += ez_find(upper_diag)
        n_xmas += ez_find(upper_diag_f)
    
    n_xmas += ez_find(col)
    n_xmas += ez_find(line)    
    n_xmas += ez_find(lower_diag)
    n_xmas += ez_find(lower_diag_f)
n_xmas
# %%
def find_mas(m):
    return bool(re.match("MAS|SAM","".join(m)))
# %%
#part 2
n_mas = 0
for i in range(n-2):
    for j in range(n-2):
        current_x = data[i:(i+3),j:(j+3)]
        diag = np.diagonal(current_x)
        other_diag = np.diagonal(np.fliplr(current_x))
        if find_mas(diag) and find_mas(other_diag):
            n_mas += 1
n_mas
        