
with open("./day-3/input.txt", "r") as input_file:
    data = input_file.read()

import regex as re

stmt = r'mul\(([0-9]+),([0-9]+)\)'
results = re.findall(stmt, data)

total = 0
for x, y in results:
    total += int(x) * int(y)

print(f"{total=}")


stmt = r'(don\'t\(\)|do\(\)|mul\(([0-9]+),([0-9]+)\))'
results = re.findall(stmt, data)

do = True
total2 = 0
for action, x, y in results:
    if action == "don't()":
        do = False
        continue
    if action == "do()":
        do = True
        continue
    if do:
        total2 += int(x) * int(y)

print(f'{total2=}')
