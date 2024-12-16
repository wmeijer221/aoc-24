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


with open(".//day-16/input.txt", "r") as input_data:
    maze = list()
    for y, line in enumerate(input_data):
        line = line.strip()
        row = ["."] * len(line)
        for x, ele in enumerate(line):
            if ele == "#":
                row[x] == "#"
            elif ele == "S":
                start = coord(x, y)
            elif ele == "E":
                target = coord(x, y)
        maze.append(line)


start_dir = coord(1, 0)
dirs = [coord(1, 0), coord(0, -1), coord(-1, 0), coord(0, 1)]

import math


def search(start: coord, start_dir: coord, target: coord):
    to_visit = {(start, start_dir)}
    cost_map = list()
    for _ in range(len(maze)):
        cost_map.append([math.inf] * len(maze[0]))
    cost_map[start.y][start.x] = 0
    while len(to_visit) > 0:
        cur_pos, cur_dir = to_visit.pop()
        for dir in dirs:
            nb = cur_pos.add(dir)
            if maze[nb.y][nb.x] == "#":
                continue
            step_cost = 1 if cur_dir == dir else 1001
            total_cost = cost_map[cur_pos.y][cur_pos.x] + step_cost
            if total_cost < cost_map[nb.y][nb.x]:
                cost_map[nb.y][nb.x] = total_cost
                to_visit.add((nb, dir))
    return cost_map[target.y][target.x]


best_cost = search(start, start_dir, target)
print(f"{best_cost=}")


# p2


def search2(start: coord, start_dir: coord, target: coord):
    to_visit = {(start, start_dir)}
    cost_map = list()
    for _ in range(len(maze)):
        cost_map.append([None] * len(maze[0]))
    cost_map[start.y][start.x] = [0]
    while len(to_visit) > 0:
        cur_pos, cur_dir = to_visit.pop()
        for dir in dirs:
            nb = cur_pos.add(dir)
            if maze[nb.y][nb.x] == "#":
                continue
            step_cost = 1 if cur_dir == dir else 1001
            total_cost = min(cost_map[cur_pos.y][cur_pos.x]) + step_cost
            if cost_map[nb.y][nb.x] is None or total_cost < min(cost_map[nb.y][nb.x]):
                to_visit.add((nb, dir))
            if cost_map[nb.y][nb.x] is None:
                cost_map[nb.y][nb.x] = []
            cost_map[nb.y][nb.x].append(total_cost)
    

    tiles = set()
    target_cost = min(cost_map[target.y][target.x])
    to_visit = {(target, target_cost)}
    while len(to_visit) > 0:
        cur_pos, cur_cost = to_visit.pop()
        tiles.add(cur_pos)
        for dir in dirs:
            nb = cur_pos.add(dir)
            nb_cost = cost_map[nb.y][nb.x]
            if nb_cost is None:
                continue
            for cost in nb_cost:
                delta = cur_cost - cost
                if delta == 1 or delta == 1001:
                    to_visit.add((nb, cost))

    return len(tiles)


tiles = search2(start, start_dir, target)
print(f'{tiles=}')

