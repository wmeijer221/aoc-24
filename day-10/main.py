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


with open(r"./day-10/input.txt", "r") as input_file:
    trailheads = set()
    map = list()
    for y, line in enumerate(input_file.readlines()):
        line = line.strip()
        entry = [0] * len(line)
        for x, ele in enumerate(line):
            entry[x] = int(ele)
            if ele == "0":
                trailheads.add(coord(x, y))
        map.append(entry)
    mapsize = coord(len(map[0]), len(map))


def is_in_bounds(pos: coord) -> bool:
    return pos.x >= 0 and pos.x < mapsize.x and pos.y >= 0 and pos.y < mapsize.y


DIRS = [coord(-1, 0), coord(0, 1), coord(1, 0), coord(0, -1)]


def find_paths(pos: coord):
    height = map[pos.y][pos.x]
    if height == 9:
        yield pos
    for dir in DIRS:
        next_pos = pos.add(dir)
        if not is_in_bounds(next_pos):
            continue
        next_height = map[next_pos.y][next_pos.x]
        if next_height == height + 1:
            yield from find_paths(next_pos)


total1 = 0
total2 = 0
for trailhead in trailheads:
    trails = list(find_paths(trailhead))
    total2 += len(trails)
    trails = set(trails)
    total1 += len(trails)

print(f"{total1=}")
print(f"{total2=}")
