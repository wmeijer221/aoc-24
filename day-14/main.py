import numpy as np
from operator import mul
from functools import reduce
from wmutils.collections.safe_dict import SafeDict
from dataclasses import dataclass


@dataclass(frozen=True)
class coord:
    x: int
    y: int

    def add(self, delta: "coord") -> "coord":
        return coord(self.x + delta.x, self.y + delta.y)

    def sub(self, delta: "coord") -> "coord":
        return coord(self.x - delta.x, self.y - delta.y)

    def scale(self, scalar: int) -> "coord":
        return coord(self.x * scalar, self.y * scalar)

    def loop(self, gridsize: "coord") -> "coord":
        return coord(self.x % gridsize.x, self.y % gridsize.y)


input_path = "./day-14/input.txt"
with open(input_path, "r") as input_data:
    data = [line.strip().split() for line in input_data]
    data = [(line[0].split("=")[1].split(","), line[1].split(
        "=")[1].split(",")) for line in data]
    data = [(coord(int(ele[0][0]), int(ele[0][1])), coord(
        int(ele[1][0]), int(ele[1][1]))) for ele in data]

if 'test' in input_path:
    mapsize = coord(11, 7)
else:
    mapsize = coord(101, 103)

# p1


def get_quadrant(pos: coord) -> int:
    center_x = mapsize.x // 2
    center_y = mapsize.y // 2
    if pos.x < center_x and pos.y < center_y:
        return 0
    elif pos.x < center_x and pos.y > center_y:
        return 1
    elif pos.x > center_x and pos.y < center_y:
        return 2
    elif pos.x > center_x and pos.y > center_y:
        return 3
    else:
        return 4


steps = 100

quadrant_count = SafeDict(default_value=0)
for pos, dir in data:
    delta = dir.scale(steps)
    target = pos.add(delta)
    target = target.loop(mapsize)
    quadrant = get_quadrant(target)
    quadrant_count[quadrant] += 1

if 4 in quadrant_count:
    del quadrant_count[4]

total1 = reduce(mul, quadrant_count.values())
print(f'{total1=}')


# p2
def draw(data, idx):
    vis = [[" " for _ in range(mapsize.x)] for _ in range(mapsize.y)]
    for pos, _ in data:
        # act_pos = pos.sub(coord(0, 2 * 36))
        act_pos = pos
        if act_pos.y < 0 or act_pos.y >= len(vis):
            continue
        vis[act_pos.y][act_pos.x] = "#"
    vis = ["".join(eles) for eles in vis]
    vis = "\n".join(vis)
    num = str(idx)
    padding = "#" * 5 + f'[{num}]' + "#" * (mapsize.x - 5 - len(num) - 2)
    vis = f'{padding}\n{vis}\n{padding}\n'
    print(vis)


new_data = [None] * len(data)
symmetric = False
runs = 0
while not symmetric:
    runs += 1
    locations = set()
    quadrant_count = SafeDict(default_value=0)
    for idx, (pos, dir) in enumerate(data):
        new_pos = pos.add(dir).loop(mapsize)
        locations.add(new_pos)
        new_data[idx] = (new_pos, dir)
        quadrant = get_quadrant(new_pos)
        quadrant_count[quadrant] += 1

    if 4 in quadrant_count:
        del quadrant_count[4]

    nbs = [coord(0, 1), coord(1, 0), coord(0, -1), coord(-1, 0)]
    has_nb = 0
    for loc in locations:
        my_nbs = 0
        for nb in nbs:
            nb_pos = loc.add(nb)
            if nb_pos in locations:
                my_nbs += 1
        if my_nbs == len(nbs):
            has_nb += 1
    has_nb /= len(locations)
    if has_nb >= 0.3:
        draw(new_data, runs)
        break

    data = new_data
