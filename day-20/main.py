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


with open('./day-20/test-input.txt', 'r') as input_file:
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
    return cost_map[target.y][target.x]


def draw_path(path: Sequence[coord]):
    my_map = deepcopy(maze)
    for pos in path:
        chr = 'x' if my_map[pos.y][pos.x] == '.' else 'O'
        my_map[pos.y][pos.x] = chr
    my_map = ["".join(ele) for ele in my_map]
    my_map = "\n".join(my_map)
    my_map = my_map.replace(".", 'q').replace('x', '.').replace('q', ' ')
    my_map += "\n"
    print(my_map)


def is_outside_map(pos: coord) -> bool:
    return pos.x < 0 or pos.x >= mapsize.x or pos.y < 0 or pos.y >= mapsize.y


def search2(start: coord, target: coord, max_cost: int):
    to_visit = {(start, True, (start,))}
    cost_map = list()
    known_paths = set()
    for _ in range(len(maze)):
        entry = list()
        for _ in range(len(maze[0])):
            entry.append([set(), set()])
        cost_map.append(entry)
    cost_map[start.y][start.x][False].add(0)
    tracker = tqdm.tqdm()
    while len(to_visit) > 0:
        tracker.n += 1
        if tracker.n % 5000 == 0:
            tracker.set_description(f'{len(to_visit)=}')
            tracker.refresh()
        cur_pos, can_cheat, my_path = to_visit.pop()
        total_cost = min(cost_map[cur_pos.y][cur_pos.x][not can_cheat])
        total_cost += 1
        pos_delta = abs(cur_pos.x - target.x) + abs(cur_pos.y - target.y)
        cost_delta = max_cost - total_cost
        if pos_delta > cost_delta or cost_delta <= 0:
            continue
        for dir in dirs:
            nb_pos = cur_pos.add(dir)
            if nb_pos in my_path or is_outside_map(nb_pos):
                continue
            is_cheating = maze[nb_pos.y][nb_pos.x] == "#"
            if is_cheating and not can_cheat:
                continue
            my_new_path = (*my_path, nb_pos,)
            h_my_new_path = hash(my_new_path)
            if h_my_new_path in known_paths:
                continue
            known_paths.add(h_my_new_path)
            has_cheated = not can_cheat or is_cheating
            cost_map[nb_pos.y][nb_pos.x][has_cheated].add(total_cost)
            can_still_cheat = not has_cheated
            to_visit.add((nb_pos, can_still_cheat, my_new_path))
            if nb_pos == target:
                yield my_new_path


original_length = day_18_search(start, end)
deltas = SafeDict(default_value=0)
total1 = 0
for my_path in search2(start, end, original_length):
    delta = original_length - (len(my_path) - 1)
    deltas[delta] += 1
    if delta >= 100:
        total1 += 1
        print(total1)

print(deltas)
