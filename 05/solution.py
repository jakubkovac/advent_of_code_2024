# %%
import numpy as np
from ast import literal_eval
# %%
with open("input.txt", "r") as f:
    lines = f.read().splitlines() 
sep_line = np.where([line == "" for line in lines])[0].flatten().item()
rules = lines[:sep_line]
pages = lines[(sep_line+1):]
# %%
middle_pages = []
for i in range(len(pages)):
    #page = pages[i].split(",")
    page = np.array(literal_eval(f"[{pages[i]}]")) #this will get me numbers already
    page_ok = True
    for rule in rules:
        rule_left,rule_right = [int(x) for x in rule.split("|")]
        ind_left = np.where(page == rule_left)[0]
        ind_right = np.where(page == rule_right)[0]
        if len(ind_left)==0 or len(ind_right)==0:
            continue
        if (ind_left > ind_right).item():
            
            page_ok = False
            break
    if page_ok:
        middle_pages.append(page[len(page)//2].item())
sum(middle_pages)
        
# %%
#part 2
middle_pages = []
for i in range(len(pages)):
    page = np.array(literal_eval(f"[{pages[i]}]"))
    page_ok = True
    for rule in rules:
        rule_left,rule_right = [int(x) for x in rule.split("|")]
        ind_left = np.where(page == rule_left)[0]
        ind_right = np.where(page == rule_right)[0]
        if len(ind_left)==0 or len(ind_right)==0:
            continue
        if (ind_left > ind_right).item():
            page_ok = False
            break
    if not page_ok:
        print(f"Page {i} is not OK.")
        updated_page = page
        check_again = True
        cycles=0
        while not page_ok:
            if not check_again:
                page_ok=True
            cycles += 1
            check_again = False
            for rule in rules:
                rule_left,rule_right = [int(x) for x in rule.split("|")]
                ind_left = np.where(page == rule_left)[0]
                ind_right = np.where(page == rule_right)[0]
                if len(ind_left)==0 or len(ind_right)==0:
                    continue
                if (ind_left > ind_right).item():
                    page_ok = False
                    updated_page[ind_left] = rule_right
                    updated_page[ind_right] = rule_left
                    check_again = True
        print(f"iterations: {cycles}\n---------")
        middle_pages.append(updated_page[len(page)//2].item())

print(sum(middle_pages))