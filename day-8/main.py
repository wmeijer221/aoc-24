from dataclasses import dataclass
from wmutils.collections.safe_dict import SafeDict


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


def is_in_bounds(pos: coord) -> bool:
    return pos.x >= 0 and pos.x < mapsize.x and pos.y >= 0 and pos.y < mapsize.y


def redraw(data, position, icon):
    data[position.y] = (
        data[position.y][0 : position.x] + icon + data[position.y][position.x + 1 :]
    )
    return data


with open("./day-8/input.txt", "r") as input_data:
    antennas = SafeDict(default_value=list)
    data = input_data.readlines()
    for y, line in enumerate(data):
        for x, ele in enumerate(line.strip()):
            if ele == ".":
                continue
            antennas[ele].append(coord(x, y))
    mapsize = coord(len(data[0].strip()), len(data))
antennas = dict(antennas)


antinodes = set()
antinodes2 = set()


def yield_until_oob(start: coord, delta: coord):
    yield start
    cand = start.add(delta)
    while is_in_bounds(cand):
        yield cand
        cand = cand.add(delta)


for key, key_antennas in antennas.items():
    for idx, a in enumerate(key_antennas):
        for idy, b in enumerate(key_antennas[idx + 1 :], start=idx + 1):
            delta = b.sub(a)

            # p2
            cand_left = yield_until_oob(b, delta)
            antinodes2 = antinodes2.union(cand_left)

            cand_right = yield_until_oob(a, delta.scale(-1))
            antinodes2 = antinodes2.union(cand_right)

            # for ele in antinodes2:
            #     data = redraw(data, ele, "#")

            # data = redraw(data, a, "X")
            # data = redraw(data, b, "X")
            # out = "".join(data)

            # print(out)
            # print()

            # data = redraw(data, a, key)
            # data = redraw(data, b, key)

            # p1
            l = b.add(delta)
            if is_in_bounds(l):
                antinodes.add(l)
            r = a.sub(delta)
            if is_in_bounds(r):
                antinodes.add(r)


print(f"{len(antinodes)=}")
print(f"{len(antinodes2)=}")


# for ele in antinodes2:
#     data = redraw(data, ele, "#")
# out = "".join(data)
# print(out)
