from dataclasses import dataclass

@dataclass(frozen=True)
class coord:
    x: int
    y: int

    def move(self, delta: "coord") -> "coord":
        return coord(self.x + delta.x, self.y + delta.y)
    def unmove(self, delta: "coord") -> "coord":
        return coord(self.x - delta.x, self.y - delta.y )


with open(r"./day-6/input.txt", "r") as input_file:
    obstacles = set()
    guard = coord(-1, -1)
    startpos = coord(-1,-1)
    data = [ele.strip() for ele in input_file.readlines()]
    
    mapsize = coord(len(data[0].strip()), len(data))

    for y, line in enumerate(data):
        for x, ele in enumerate(line):
            entity = coord(x,y)
            if ele == "#":
                obstacles.add(entity)
            elif ele == "^":
                guard = entity
                startpos = coord(entity.x, entity.y)

guard_direction = coord(0, -1)
dir_mapping1 = [coord(-1, 0), coord(0, -1), coord(1, 0), coord(0, 1)]
dir_mapping = {dir_mapping1[i]: dir_mapping1[i+1] for i in range(len(dir_mapping1)-1)}
dir_mapping[dir_mapping1[-1]] = dir_mapping1[0]

positions = set()
the_path = list()

def is_in_bounds(pos: coord) -> bool:
    return  pos.x >= 0 and pos.x < mapsize.x and pos.y >= 0 and pos.y < mapsize.y

while is_in_bounds(guard):
    data[guard.y] = data[guard.y][0:guard.x] + "X" + data[guard.y][guard.x + 1:]
    # out = "\n".join(data)
    # print(out)

    positions.add(guard)
    next_guard = guard.move(guard_direction)
    if next_guard in obstacles:
        the_path.append((guard, guard_direction))
        guard_direction = dir_mapping[guard_direction]
    else:
        guard = next_guard


def redraw(data, position, icon):
    data[position.y] = data[position.y][0:position.x] + icon + data[position.y][position.x + 1:]
    return data
def clamp(x, a, b):
    if x < a:
        return a
    if x > b: 
        return b
    return x


print(f'{len(positions)=}')
from copy import deepcopy
valid_options = set()
for idx, (bump, bumpdir) in enumerate(the_path):
    next_bumpdir = dir_mapping[bumpdir]
    option = bump.move(next_bumpdir)
    while option not in obstacles and is_in_bounds(option):
        if option == startpos:
            option = option.move(next_bumpdir)
            continue

        for (old_bump, old_bumpdir) in the_path[:idx]:

            
            # opt_data = deepcopy(data)
            # opt_data = redraw(opt_data, option, "O")
            # opt_data = redraw(opt_data, old_bump, "G")
            # opt_data = redraw(opt_data, bump, "B")
            # out = "\n".join(opt_data) + "\n"
            # print(out)
            # print()



            next_next_bumpdir = dir_mapping[next_bumpdir]
            if old_bumpdir != next_next_bumpdir:
                continue
            
            option_bump = option.unmove(next_bumpdir)
            
            if old_bumpdir.y != 0 and old_bump.x == option_bump.x and clamp(old_bump.y - option_bump.y, -1, 1) == old_bumpdir.y:
                valid_options.add(option)
            elif old_bumpdir.x != 0 and old_bump.y == option_bump.y and clamp(old_bump.x - option_bump.x, -1, 1) == old_bumpdir.x:
                valid_options.add(option)
        option = option.move(next_bumpdir)


print(f"{len(valid_options)=}")
