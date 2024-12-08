# %%
import numpy as np

with open("input.txt") as f:
    data = f.read().splitlines()
for i in range(len(data)):
    data[i] = np.array([int(x) for x in data[i].split(" ")])
# %%
def is_safe(reports):
    d = reports[:-1] - reports[1:]
    d_abs = np.abs(d)
    if all(d_abs>=1) and all(d_abs<=3) and (all(d>0) or all(d<0)):
        return True
    return False
# %%
n_safe = 0
for i in range(len(data)):
    n_safe += is_safe(data[i])
n_safe
# %%
#part 2
n_safe = 0
for i in range(len(data)):
    reports = data[i]
    s = is_safe(reports)
    if s:
        n_safe += s
    else:
        for j in range(len(reports)):
            s = is_safe(np.delete(reports,j))
            if s:
                n_safe += 1
                break
n_safe