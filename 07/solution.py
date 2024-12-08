# %%
#in_file = "sample.txt"
in_file = "input.txt"
with open(in_file) as f:
    data = f.read().splitlines()
data
# %%
def skip_too_high(numbers, answer):
    if any([n > answer for n in numbers]):
        return True
    return False
# %%
def is_possible(numbers, answer, allow_concat = False):
    if len(numbers) == 1:
        return numbers[0] == answer
    if is_possible([numbers[0]+numbers[1]]+numbers[2:], answer, allow_concat):
        return True
    if is_possible([numbers[0]*numbers[1]]+numbers[2:], answer, allow_concat):
        return True
    if allow_concat and is_possible([int(str(numbers[0])+str(numbers[1]))]+numbers[2:], answer, allow_concat):
        return True
    return False

total = 0
total2 = 0
for line in data:
    answer, numbers = line.split(": ")
    answer = int(answer)
    numbers = [int(x) for x in numbers.split(" ")]
    if not skip_too_high(numbers, answer):
        is_p = is_possible(numbers, answer)
        is_p2 = is_possible(numbers, answer, allow_concat=True)
        total += is_p*answer
        total2 += is_p2*answer
print(total)
print(total2)