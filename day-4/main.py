
from itertools import product
with open(r'./day-4/input.txt', 'r') as input_file:
    data = [line.strip() for line in input_file.readlines()]

search_term = "XMAS"
height = len(data)
width = len(data[0])


def search(x, y, dx, dy, idx, search_term) -> bool:
    if x < 0 or x >= width or y < 0 or y >= height:
        return False
    ele = data[y][x]
    target = search_term[idx]
    if ele != target:
        return False
    if idx + 1 < len(search_term):
        return search(x + dx, y + dy, dx, dy, idx + 1, search_term)
    return True


total = 0
for x, y in product(range(width), range(height)):
    for dx, dy in product(range(-1, 2), range(-1, 2)):
        if dx == dy and dx == 0:
            continue
        if search(x, y, dx, dy, 0, search_term):
            total += 1

print(f'{total=}')


new_search_term = "MAS"
new_search_term2 = "SAM"
new_total = 0
for x, y in product(range(width), range(height)):
    if (search(x, y, 1, 1, 0, new_search_term) or search(x, y, 1, 1, 0, new_search_term2)) and (search(x, y + 2, 1, -1, 0, new_search_term) or search(x, y + 2, 1, -1, 0, new_search_term2)):
        new_total += 1

print(f'{new_total=}')
