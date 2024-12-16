# %%
import re

import numpy as np
from scipy.optimize import LinearConstraint, milp

# %%
in_file = "sample.txt"
in_file = "input.txt"
with open(in_file) as f:
    data = f.read()

# %%
pattern = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")


def parse_input(data, adjust_prize=0):
    problems = data.strip().split("\n\n")
    out = []
    for problem in problems:
        button_a, button_b, prize = problem.splitlines()
        ax, ay = re.findall(pattern, button_a)[0]
        bx, by = re.findall(pattern, button_b)[0]
        prizex, prizey = re.findall(r"Prize: X=(\d+), Y=(\d+)", prize)[0]
        out.append(
            (
                np.array([[int(ax), int(bx)], [int(ay), int(by)]]),
                np.array([int(prizex) + adjust_prize, int(prizey) + adjust_prize]),
            )
        )
    return out


data_part1 = parse_input(data)
data_part2 = parse_input(data, adjust_prize=10000000000000)


# %%
def full_solver(problem):
    a, b = problem[0][0]  # First row
    c, d = problem[0][1]  # Second row
    detA = a * d - b * c
    if detA != 0:
        return naive_solution(problem)
    else:
        return milp_solver(problem)


def naive_solution(problem, cost=[3, 1], tolerance=1e-5):
    M = problem[0]
    P = problem[1]
    R = np.round(np.linalg.solve(M, P))
    return R @ (3, 1) if (P == R @ M.T).all() else 0


def milp_solver(problem, cost=[3, 1], return_full=False):
    cost = np.array(cost)
    A = problem[0]
    b_u = problem[1]
    b_l = b_u
    constraints = LinearConstraint(A, b_l, b_u)
    integrality = np.ones_like(cost)
    res = milp(
        c=cost,
        constraints=constraints,
        integrality=integrality,
        options={"presolve": True},
    )
    if return_full:
        return res
    if res.fun is None:
        return 0
    return int(res.fun)


# %%

print(int(sum(milp_solver(x) for x in data_part1)))
print(int(sum(full_solver(x) for x in data_part1)))

# %%

print(int(sum(milp_solver(x) for x in parse_input(data, adjust_prize=10000000000000))))
print(int(sum(full_solver(x) for x in parse_input(data, adjust_prize=10000000000000))))
# %%

# %%
