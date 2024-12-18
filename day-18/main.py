import networkx as nx
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


data_path = './day-18/input.txt'
with open(data_path, 'r') as input_data:
    data = [line.strip().split(",") for line in input_data]
    data = [coord(int(ele[0]), int(ele[1])) for ele in data]

is_test = 'test' in data_path
mapsize = coord(7, 7) if is_test else coord(71, 71)
max_bytes = 12 if is_test else 1024

start = coord(0, 0)
target = coord(6, 6) if is_test else coord(70, 70)

nbs = [coord(-1, 0), coord(0, 1), coord(1, 0), coord(0, -1)]

obstacles = set()
path = set()

obstacles = obstacles.union(data[:max_bytes])

# p1


def search(start: coord, target: coord):
    to_visit = {start}
    cost_map = list()
    for _ in range(mapsize.y):
        cost_map.append([math.inf] * mapsize.x)
    cost_map[start.y][start.x] = 0
    while len(to_visit) > 0:
        cur_pos = to_visit.pop()
        for dir in nbs:
            nb = cur_pos.add(dir)
            if nb in obstacles:
                continue
            if nb.x < 0 or nb.x >= mapsize.x or nb.y < 0 or nb.y >= mapsize.y:
                continue
            step_cost = 1
            total_cost = cost_map[cur_pos.y][cur_pos.x] + step_cost
            if total_cost < cost_map[nb.y][nb.x]:
                cost_map[nb.y][nb.x] = total_cost
                to_visit.add(nb)
    return cost_map[target.y][target.x]


best_cost = search(start, target)
print(f"{best_cost=}")


G: nx.Graph = nx.Graph()
for y in range(mapsize.y):
    for x in range(mapsize.x):
        pos = coord(x, y)
        idx = pos.y * mapsize.x + pos.x
        for nb in nbs:
            nb_pos = pos.add(nb)
            if nb_pos.x < 0 or nb_pos.x >= mapsize.x or nb_pos.y < 0 or nb_pos.y >= mapsize.y:
                continue
            idy = nb_pos.y * mapsize.x + nb_pos.x
            G.add_edge(idx, idy)

source_idx = start.y * mapsize.x + start.x
target_idx = target.y * mapsize.x + target.x

# print(len(G.nodes))

is_connected = True
for i, pos in enumerate(data):
    # print(i)
    idx = pos.y * mapsize.x + pos.x
    for nb in nbs:
        other_pos = pos.add(nb)
        idy = other_pos.y * mapsize.x + other_pos.x
        if G.has_edge(idy, idx):
            G.remove_edge(idx, idy)
        try:
            nx.astar_path(G, source_idx, target_idx)
        except nx.NetworkXNoPath:
            is_connected = False
            break
    if not is_connected:
        break

print(f'res2={pos.x},{pos.y}')
