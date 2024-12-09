# %%
import numpy as np
in_file = "sample.txt"
in_file = "sample2.txt"
in_file = "input.txt"
with open(in_file) as f:
    data = f.read()
data = np.array(list(data), dtype = int)
if len(data) % 2 != 0:
    data = np.append(data, 0)
# %%
# every odd index indicates the number of blocks available
# every even index indicates number of blocks
# the position of the block indicates the id
memory_blocks = data[np.ix_(*[range(0,i,2) for i in data.shape])]
empty_blocks = data[np.ix_(*[range(1,i,2) for i in data.shape])]
print(memory_blocks)
print(empty_blocks)
# %%
out = []
n = len(memory_blocks)
j = n-1
for i in range(n):
    print(f"Filling gap: {i}")
    out = out + [i]*memory_blocks[i]
    memory_blocks[i] = 0
    n_empty_block = int(empty_blocks[i])
    n_fills = 0
    if n_empty_block >0 and j >0:
        while n_fills < n_empty_block and j >0:
            if memory_blocks[j]>=n_empty_block:
                res_blocks = memory_blocks[j]-n_empty_block
                n_fills = n_empty_block
                out = out + [j]*n_empty_block
                memory_blocks[j]=res_blocks
            else:
                # add residuals
                res_blocks = n_empty_block - memory_blocks[j]
                out = out + [j]*memory_blocks[j]
                memory_blocks[j] = 0
                n_empty_block = res_blocks
                j = j - 1
np.sum(np.multiply(np.array(out), np.array(range(len(out)))))
# %%
in_file = "input.txt"
with open(in_file) as f:
    data = f.read()
data = np.array(list(data), dtype = int)
if len(data) % 2 != 0:
    data = np.append(data, 0)
memory_blocks = data[np.ix_(*[range(0,i,2) for i in data.shape])]
empty_blocks = data[np.ix_(*[range(1,i,2) for i in data.shape])]

def print_memory(data):
    print("".join([str(x).replace("-1",".") for x in data]))
    
n = len(memory_blocks)
j = n-1
full_list = []
gap_indices = []
memory_indices = []
for i in range(n):
    y = len(full_list)
    y2 = y+int(memory_blocks[i])
    memory_indices = memory_indices + [(y, y2)]
    full_list = full_list + [i]*memory_blocks[i]
    x = len(full_list)
    if int(empty_blocks[i]) == 0:
        gap_indices = gap_indices + [None]
    else:
        gap_indices = gap_indices + [(x,x+int(empty_blocks[i]))]
    full_list = full_list + [-1]*empty_blocks[i]
# %%
for j in reversed(range(n)):
    if j % 100 == 0:
        print(f"{j}/{n}")
    current_block = memory_blocks[j]
    for i in range(j):
        if current_block <= empty_blocks[i]:
            d_size = empty_blocks[i] - current_block
            full_list[slice(*gap_indices[i])] = [j]*current_block + [-1]*d_size
            full_list[slice(*memory_indices[j])] = [-1]*current_block
            if d_size >0:
                gap_indices[i] = (int(gap_indices[i][0]+current_block),gap_indices[i][1])
            else:
                gap_indices[i] = None                  
            
            empty_blocks[i] = empty_blocks[i]-current_block
            #print_memory(full_list)
            break

my_list = [0 if x == -1 else x for x in full_list]

# %%
np.sum(np.multiply(np.array(my_list), np.array(range(len(my_list)))))
# %%
