
from collections.abc import Mapping
from dataclasses import dataclass
from typing import List, Set
from wmutils.collections.safe_dict import SafeDict


@dataclass
class Gate:
    op_a: str
    op_b: str
    gate: str
    out: str


with open("./day-24/input.txt", 'r') as input_file:
    all_registers: Mapping[str, int] = dict()
    new_registers: Set[str] = set()
    while len(line := next(input_file).strip()) > 0:
        register, value = line.split()
        value = int(value)
        register = register[:-1]
        all_registers[register] = value
        new_registers.add(register)

    subscriptions: SafeDict[str, List[Gate]] = SafeDict(default_value=list)
    gates = list()
    for line in input_file:
        elements = line.strip().split()
        in_a = elements[0]
        in_b = elements[2]
        gate = elements[1]
        out = elements[4]
        gate = Gate(in_a, in_b, gate, out)
        gate_idx = len(gates)
        gates.append(gate)
        subscriptions[in_a].append(gate_idx)
        subscriptions[in_b].append(gate_idx)


ops = {
    'XOR': lambda a, b: 1 if a != b else 0,
    "OR": lambda a, b: 1 if a + b > 0 else 0,
    "AND": lambda a, b: 1 if a + b == 2 else 0
}


def registers_to_number(reg_key: str) -> int:
    z_registers = [key for key in all_registers.keys() if key[0] == reg_key]
    z_registers = sorted(z_registers)

    total1 = 0
    for exp, reg in enumerate(z_registers):
        bit = all_registers[reg]
        val = bit * 2 ** exp
        total1 += val
    return total1


x = registers_to_number('x')
y = registers_to_number('y')
target_z = x + y
print(target_z)


def simulate(new_registers, gates, subscriptions):
    while len(new_registers) > 0:
        register = new_registers.pop()
        for sub_idx in subscriptions[register]:
            sub = gates[sub_idx]
            if not (sub.op_a in all_registers and sub.op_b in all_registers):
                continue
            op = ops[sub.gate]
            out = op(all_registers[sub.op_a], all_registers[sub.op_b])
            all_registers[sub.out] = out
            new_registers.add(sub.out)

    total1 = registers_to_number('z')
    return total1


total1 = simulate(new_registers, gates, subscriptions)
print(f'{total1=}')


# def triangular_iter(data, repeats=2, __repeat=0, __start=0):
#     for idx, ele in enumerate(data[__start:]):
#         if __repeat < repeats:
#             children = triangular_iter(
#                 data, repeats, __repeat+1, __start + idx + 1)
#             yield from ((ele, *child) for child in children)
#         else:
#             yield (ele,)


# print(len(gates))

# q = triangular_iter([gate.out for gate in gates], 8)
# print(len(list(q)))
