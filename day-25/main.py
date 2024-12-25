
with open('./day-25/input.txt', 'r') as input_file:
    keys = list()
    locks = list()
    current_key = [-1] * 5
    for line in input_file:
        line = line.strip()
        if len(line) == 0:
            if all_filled:
                keys.append(tuple(current_key))
            else:
                locks.append(tuple(current_key))
            current_key = [-1] * 5
            continue
        all_filled = True
        for idx, ele in enumerate(line):
            if ele == '#':
                current_key[idx] += 1
            else:
                all_filled = False
    keys.append(tuple(current_key))


total1 = 0
for lock in locks:
    for key in keys:
        fits = (a + b for a, b in zip(lock, key))
        fits = all(fit <= 5 for fit in fits)
        if fits:
            total1 += 1
print(f'{total1=}')
