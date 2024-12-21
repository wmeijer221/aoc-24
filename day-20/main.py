import itertools
import tqdm
from collections.abc import Sequence
from copy import deepcopy
from wmutils.collections.safe_dict import SafeDict
import math
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


input_path = './day-20/input.txt'
with open(input_path, 'r') as input_file:
    maze = list()
    start = None
    end = None
    for y, line in enumerate(input_file):
        line = line.strip()
        row = ["."] * len(line)
        for x, ele in enumerate(line):
            if ele == "#":
                row[x] = "#"
            if ele == 'S':
                start = coord(x, y)
            if ele == 'E':
                end = coord(x, y)
        maze.append(row)
mapsize = coord(len(maze[0]), len(maze))

dirs = [coord(-1, 0), coord(0, 1), coord(1, 0), coord(0, -1)]


def day_18_search(start: coord, target: coord):
    to_visit = {start}
    cost_map = list()
    for _ in range(mapsize.y):
        cost_map.append([math.inf] * mapsize.x)
    cost_map[start.y][start.x] = 0
    while len(to_visit) > 0:
        cur_pos = to_visit.pop()
        for dir in dirs:
            nb = cur_pos.add(dir)
            if maze[nb.y][nb.x] == "#":
                continue
            if nb.x < 0 or nb.x >= mapsize.x or nb.y < 0 or nb.y >= mapsize.y:
                continue
            step_cost = 1
            total_cost = cost_map[cur_pos.y][cur_pos.x] + step_cost
            if total_cost < cost_map[nb.y][nb.x]:
                cost_map[nb.y][nb.x] = total_cost
                to_visit.add(nb)
    return cost_map


def draw_path(path: Sequence[coord]):
    elements = set(path)

    out = ""
    for y in range(mapsize.y):
        for x in range(mapsize.x):
            pos = coord(x, y)
            if pos in elements:
                if maze[pos.y][pos.x] == "#":
                    out = f'{out}O'
                else:
                    out = f'{out}.'
            else:
                if maze[pos.y][pos.x] == "#":
                    out = f'{out}#'
                else:
                    out = f'{out} '
        out = f'{out}\n'
    print(out)


def draw_empty(elements: Sequence[coord]):
    elements = set(elements)

    max_x = max(ele.x for ele in elements)
    max_y = max(ele.y for ele in elements)

    out = ""
    for y in range(max_y + 2):
        for x in range(max_x + 2):
            pos = coord(x, y)
            if pos in elements:
                out = f'{out}#'
            else:
                out = f'{out}.'
        out = f'{out}\n'
    print(out)


cost_map = day_18_search(start, end)


def get(pos: coord):
    return cost_map[pos.y][pos.x]


def is_not_in_bounds(nb: coord):
    return nb.x < 0 or nb.x >= mapsize.x or nb.y < 0 or nb.y >= mapsize.y


total1 = 0
for y in range(mapsize.y):
    for x in range(mapsize.x):
        pos = coord(x, y)
        if maze[pos.y][pos.x] != "#":
            continue
        for i, dir_a in enumerate(dirs):
            for dir_b in dirs[i+1:]:
                nb_pos_a = pos.add(dir_a)
                nb_pos_b = pos.add(dir_b)
                if is_not_in_bounds(nb_pos_a) or is_not_in_bounds(nb_pos_b):
                    continue
                cost_a = cost_map[nb_pos_a.y][nb_pos_a.x]
                cost_b = cost_map[nb_pos_b.y][nb_pos_b.x]
                if cost_a == math.inf or cost_b == math.inf:
                    continue
                cost_gain = abs(cost_a - cost_b)
                cost_gain -= 2
                if cost_gain >= 100:
                    total1 += 1

# 1329 is too low
# 1355
print(f'{total1=}')


def targets(pos: coord, radius: coord):
    for x in range(-radius, radius + 1):
        for y in range(radius - abs(x) + 1):
            yield coord(pos.x + x, pos.y + y)
            yield coord(pos.x + x, pos.y - y)
            if x != 0:
                yield coord(pos.x - x, pos.y + y)
            if y != 0:
                yield coord(pos.x - x, pos.y - y)


def bounded_targets(pos: coord, radius: int):
    for ele in targets(pos, radius):
        if is_not_in_bounds(ele):
            continue
        yield ele


def valid_bounded_targets(pos: coord, radius: int):
    q = set()
    for ele in bounded_targets(pos, radius):
        if maze[ele.y][ele.x] == "#":
            continue
        if ele in q:
            continue
        q.add(ele)
        yield ele


# draw_path(valid_bounded_targets(start, 6))
# print(list(valid_bounded_targets(start, 6)))

is_test = 'test' in input_path
radius = 20
threshold = 50 if is_test else 100

total2 = 0
# scores = SafeDict(default_value=0)
for y in range(mapsize.y):
    for x in range(mapsize.x):
        pos = coord(x, y)
        if maze[pos.y][pos.x] == "#":
            continue
        my_cost = cost_map[pos.y][pos.x]
        for nb_pos in valid_bounded_targets(pos, radius):
            nb_cost = cost_map[nb_pos.y][nb_pos.x]
            cost_gain = nb_cost - my_cost
            if cost_gain < 0:
                continue
            cost_gain -= abs(pos.x - nb_pos.x) + abs(pos.y - nb_pos.y)
            # scores[cost_gain] += 1
            if cost_gain >= threshold:
                total2 += 1

# 285 example.

# 2366599 too high
# 233266 too low
# 466532 too low
print(f'{total2=}')
# print(scores)
