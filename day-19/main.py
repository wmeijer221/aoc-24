import tqdm
with open('./day-19/input.txt', 'r') as input_file:
    available = next(input_file).strip().split(", ")

    desired = list()
    next(input_file)
    desired = [line.strip() for line in input_file]


import regex as re

expr = "|".join(available)
expr = f"^(({expr})+)$"
expr = re.compile(expr)

total1 = 0
for line in desired:
    matches = expr.match(line)
    if matches:
        total1 += 1

print(f'{total1=}')

# p2


def find_all(target: str):
    to_visit = list()
    to_visit.append([])
    while len(to_visit) > 0:
        current_eles = to_visit.pop()
        for opt in available:
            nxt_eles = [*current_eles, opt]
            nxt = "".join(nxt_eles)
            if nxt == target:
                nxt = ""
                yield nxt_eles
            elif target.startswith(nxt):
                to_visit.append(nxt_eles)


old = dict()


def find2(target: str):
    if len(target) == 0:
        return 1
    if target in old:
        return old[target]
    all_options = 0
    for opt in available:
        mtch = re.match(opt, target)
        if mtch is None:
            continue
        start_idx, end_idx = mtch.span()

        prefix = target[:start_idx]
        suffix = target[end_idx:]

        ps_options = find2(prefix) * find2(suffix)
        all_options += ps_options
    old[target] = all_options
    return all_options


total2 = 0
for line in tqdm.tqdm(desired):
    tot = find2(line)
    total2 += tot
print(f'{total2=}')
