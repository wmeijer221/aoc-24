
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

    def loop(self, gridsize: "coord") -> "coord":
        return coord(self.x % gridsize.x, self.y % gridsize.y)


with open('./day-15/input.txt', 'r') as input_data:
    read_input = False
    warehouse = []
    warehouse2 = []
    input = []
    robot = coord(-1, -1)
    robot2 = coord(-1, -1)
    for y, line in enumerate(input_data):
        line = line.strip()
        if len(line) == 0:
            read_input = True
            continue
        if not read_input:
            row = ["."] * len(line)
            row2 = ["."] * (2 * len(line))
            for x, ele in enumerate(line):
                if ele == "@":
                    robot = coord(x, y)
                    robot2 = coord(2 * x, y)
                else:
                    row[x] = ele
                    if ele == "#":
                        row2[x * 2] = "#"
                        row2[x * 2 + 1] = "#"
                    elif ele == 'O':
                        row2[x * 2] = "["
                        row2[x * 2 + 1] = "]"
            warehouse.append(row)
            warehouse2.append(row2)
        else:
            input.extend(line)


mapping = {'^': coord(0, -1), ">": coord(1, 0),
           "<": coord(-1, 0), "v": coord(0, 1)}


# p1
def find_boxes_to_wall(pos: coord, dir: coord) -> Tuple[bool, Sequence[coord]]:
    boxes = []
    new_pos = pos.add(dir)
    tile = warehouse[new_pos.y][new_pos.x]
    if tile == '.':
        return False, boxes
    elif tile == '#':
        return True, boxes
    elif tile == 'O':
        boxes.append(new_pos)
    blocked, next_boxes = find_boxes_to_wall(new_pos, dir)
    boxes.extend(next_boxes)
    return blocked, boxes


for inp in input:
    dir = mapping[inp]
    blocked, boxes = find_boxes_to_wall(robot, dir)
    if blocked:
        continue
    for box in boxes:
        new_box = box.add(dir)
        warehouse[new_box.y][new_box.x] = 'O'
    if len(boxes) > 0:
        warehouse[boxes[0].y][boxes[0].x] = '.'
    robot = robot.add(dir)


def draw(data, robot: coord = None):
    out = ""
    for y, row in enumerate(data):
        if robot is None or y != robot.y:
            r = "".join(row)
        else:
            r = "".join(row[:robot.x]) + "@" + "".join(row[robot.x+1:])
        out += r + "\n"
    print(out)


draw(warehouse)


total1 = 0
for y, row in enumerate(warehouse):
    for x, ele in enumerate(row):
        if ele == 'O':
            total1 += 100 * y + x
print(f"{total1=}")


# p2
def find_boxes_to_wall2(pos: coord, dir: coord) -> Tuple[bool, Sequence[coord]]:
    boxes = []
    new_pos = pos.add(dir)
    tile = warehouse2[new_pos.y][new_pos.x]
    if tile == '.':
        return False, boxes
    elif tile == '#':
        return True, boxes

    if tile == '[':
        other_tile = new_pos.add(coord(1, 0))
        my_box = (new_pos, other_tile)
    elif tile == ']':
        other_tile = new_pos.add(coord(-1, 0))
        my_box = (other_tile, new_pos)

    boxes.append(my_box)

    if dir.x == 0:
        blocked1, boxes1 = find_boxes_to_wall2(my_box[0], dir)
        blocked2, boxes2 = find_boxes_to_wall2(my_box[1], dir)

        boxes.extend(boxes1)
        boxes.extend(boxes2)
        blocked = blocked1 or blocked2

    elif dir.x == 1:
        # new_new_pos = my_box[1].add(dir)
        blocked, boxes1 = find_boxes_to_wall2(my_box[1], dir)
        boxes.extend(boxes1)

    else:
        # new_new_pos = my_box[0].add(dir)
        blocked, boxes1 = find_boxes_to_wall2(my_box[0], dir)
        boxes.extend(boxes1)

    return blocked, boxes


for inp in input:
    dir = mapping[inp]
    blocked, boxes = find_boxes_to_wall2(robot2, dir)
    if blocked:
        continue

    for box in boxes:
        warehouse2[box[0].y][box[0].x] = "."
        warehouse2[box[1].y][box[1].x] = "."
    for box in boxes:
        lhs = box[0].add(dir)
        rhs = box[1].add(dir)
        warehouse2[lhs.y][lhs.x] = '['
        warehouse2[rhs.y][rhs.x] = ']'

    robot2 = robot2.add(dir)

draw(warehouse2, robot2)


total2 = 0
for y, row in enumerate(warehouse2):
    for x, ele in enumerate(row):
        if ele == '[':
            total2 += 100 * y + x
print(f"{total2=}")
