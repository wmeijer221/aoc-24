from dataclasses import dataclass
from collections.abc import Sequence


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


@dataclass
class Machine:
    a: coord
    b: coord
    prize: coord


with open("./day-13/input.txt", "r") as input_data:
    machines: Sequence[Machine] = []
    machines2: Sequence[Machine] = []
    cur_a: coord
    cur_b: coord
    cur_prize: coord
    for line in input_data.readlines():
        line = line.strip()
        if len(line) == 0:
            machines.append(Machine(cur_a, cur_b, cur_prize))
            machines2.append(Machine(cur_a, cur_b, cur_prize.add(
                coord(10000000000000, 10000000000000))))
            continue
        tokens = line.split()
        if "A:" in line:
            cur_a = coord(int(tokens[2].split("+")[1][:-1]),
                          int(tokens[3].split("+")[1]))
        elif "B:" in line:
            cur_b = coord(int(tokens[2].split("+")[1][:-1]),
                          int(tokens[3].split("+")[1]))
        else:
            cur_prize = coord(
                int(tokens[1].split("=")[1][:-1]), int(tokens[2].split("=")[1]))

cost_a = 3
cost_b = 1


def get(machine: Machine):
    x = (machine.prize.x * machine.b.y - machine.b.x * machine.prize.y) / \
        (machine.a.x * machine.b.y - machine.a.y * machine.b.x)
    y = (machine.a.x * machine.prize.y - machine.a.y * machine.prize.x) / \
        (machine.a.x * machine.b.y - machine.a.y * machine.b.x)
    return x, y


total1 = 0
for machine in machines:
    x, y = get(machine)
    if int(x) == x and int(y) == y:
        cost = cost_a * x + cost_b * y
        total1 += cost

print(f'{int(total1)=}')

total2 = 0
for machine in machines2:
    x, y = get(machine)
    if int(x) == x and int(y) == y:
        cost = cost_a * x + cost_b * y
        total2 += cost


print(f'{int(total2)=}')
