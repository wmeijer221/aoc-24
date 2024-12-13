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


with open("./day-13/test-input.txt", "r") as input_data:
    machines: Sequence[Machine] = []
    cur_a: coord
    cur_b: coord
    cur_prize: coord
    for line in input_data.readlines():
        line = line.strip()
        if len(line) == 0:
            machines.append(Machine(cur_a, cur_b, cur_prize))
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


# for machine in machines:
#     x1 = machine.prize.x / machine.a.x


#     # x1 = (-machine.prize.x - ((machine.b.x * machine.prize.x) /
#     #       machine.a.x)) / (machine.b.x - machine.a.x)
#     print(x1)