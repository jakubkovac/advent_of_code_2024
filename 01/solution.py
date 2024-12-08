# %%
import numpy as np
data = np.loadtxt("input.txt", dtype="int").T
# %%
print(np.sum(np.abs(np.sort(data[0]) - np.sort(data[1]))))
# %%
sim = 0
for x in data[0]:
    sim += x*len(np.where(data[1]==x)[0])
print(sim)