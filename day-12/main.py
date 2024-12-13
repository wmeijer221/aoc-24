from collections.abc import Sequence
from typing import Tuple
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


with open("./day-12/input.txt", "r") as input_file:
    data = [[ele for ele in line.strip()] for line in input_file.readlines()]

mapsize = coord(len(data[0]), len(data))


def is_in_bounds(pos: coord) -> bool:
    return pos.x >= 0 and pos.x < mapsize.x and pos.y >= 0 and pos.y < mapsize.y


def get(pos: coord) -> str:
    return data[pos.y][pos.x]


neighbors = [coord(-1, 0), coord(1, 0), coord(0, -1), coord(0, 1)]

# p1
areas = SafeDict(default_value=0)
perimiters = SafeDict(default_value=0)
finished = set()


def count(pos: coord):
    my_lab = get(pos)
    yield (0, 1)
    finished.add(pos)
    for nb in neighbors:
        nb_pos = pos.add(nb)
        if not is_in_bounds(nb_pos):
            yield (1, 0)
            continue
        nb_lab = get(nb_pos)
        if my_lab != nb_lab:
            yield (1, 0)
        elif nb_pos not in finished:
            yield from count(nb_pos)


total1 = 0
for x in range(mapsize.x):
    for y in range(mapsize.y):
        pos = coord(x, y)
        if pos in finished:
            continue
        results = list(count(pos))
        perimiter = sum(e[0] for e in results)
        area = sum(e[1] for e in results)
        q = perimiter * area
        total1 += q

print(f"{total1=}")


# p2

finished2 = set()


def count2(pos: coord):
    my_lab = get(pos)
    yield (0, 1)
    finished2.add(pos)
    for nb in neighbors:
        nb_pos = pos.add(nb)
        if not is_in_bounds(nb_pos):
            yield ((pos, nb_pos), 0)
            continue
        nb_lab = get(nb_pos)
        if my_lab != nb_lab:
            yield ((pos, nb_pos), 0)
        elif nb_pos not in finished2:
            yield from count2(nb_pos)


def handle_perimiters(perimiters: Sequence[Tuple[coord, coord]]):
    panels = list()

    for (pos_a, pos_b) in perimiters:
        possible_idxs = []
        valid = True
        if pos_a.y == pos_b.y:
            for idx, panel in enumerate(panels):
                for (ele_a, ele_b) in panel:
                    if abs(ele_a.y - pos_a.y) == 1 and (pos_a.x - pos_b.x) == (ele_a.x - ele_b.x) and pos_a.x == ele_a.x:
                        possible_idxs.append(idx)
                        break

        elif pos_a.x == pos_b.x:
            for idx, panel in enumerate(panels):
                for (ele_a, ele_b) in panel:
                    if abs(ele_a.x - pos_a.x) == 1 and (pos_a.y - pos_b.y) == (ele_a.y - ele_b.y) and pos_a.y == ele_a.y:
                        possible_idxs.append(idx)
                        break

        else:
            valid = False

        if valid:
            if len(possible_idxs) == 0:
                panels.append([(pos_a, pos_b)])
            elif len(possible_idxs) == 1:
                panels[possible_idxs[0]].append((pos_a, pos_b))
            else:
                possible_idxs = sorted(possible_idxs)
                target_idx = possible_idxs[0]
                panels[target_idx].append((pos_a, pos_b))
                sources = sorted(possible_idxs[1:], reverse=True)
                for source_idx in sources:
                    panels[target_idx].extend(panels[source_idx])
                    panels = [*panels[:source_idx], *panels[source_idx + 1:]]

    return len(panels)


total2 = 0
for y in range(mapsize.y):
    for x in range(mapsize.x):
        pos = coord(x, y)
        if pos in finished2:
            continue
        results = list(count2(pos))
        area = sum(e[1] for e in results)
        perimiters = [e[0] for e in results if e[0] != 0]
        label = get(perimiters[0][0])
        perimiter = handle_perimiters(perimiters)
        q = perimiter * area
        total2 += q

print(f"{total2=}")
