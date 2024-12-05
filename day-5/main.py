
with open('./day-5/input.txt', 'r') as input_file:
    data = input_file.readlines()
    order_rules = []
    idx = 0
    for line in data:
        idx += 1
        line = line.strip()
        if len(line) == 0:
            break
        left, right = line.split("|")
        left = int(left)
        right = int(right)
        order_rules.append((left, right))

    data = [[int(ele) for ele in line.strip().split(",")] for line in data[idx:]]

from collections.abc import Mapping
def sort_this(entry: list[int], idxs: Mapping[int, int]) -> bool:
    flag = False
    for a, b in order_rules:
        if a not in idxs or b not in idxs:
            continue
        if idxs[a] < idxs[b]:
            continue
        tmp = entry[idxs[a]]
        entry[idxs[a]] = entry[idxs[b]]
        entry[idxs[b]] = tmp
        tmp2 = idxs[a]
        idxs[a] = idxs[b]
        idxs[b] = tmp2
        flag = True
    if flag:
        return sort_this(entry, idxs)
    return entry
        


count = 0
count2 = 0
for entry in data:
    idxs = {ele: idx for idx, ele in enumerate(entry)}

    valid = all(a not in idxs or b not in idxs or idxs[a] < idxs[b] for a, b in order_rules )
    if valid:
        mid = int(len(entry) / 2)
        count += entry[mid]
        continue

    sorted= sort_this(entry , idxs)
    mid = int(len(entry) / 2)
    count2 += entry[mid]

print(f'{count=}')
print(f'{count2=}')
