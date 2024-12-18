
with open("./day-17/input.txt", 'r') as input_data:
    lines = input_data.readlines()
    reg_a = int(lines[0].strip().split()[-1])
    reg_b = int(lines[1].strip().split()[-1])
    reg_c = int(lines[2].strip().split()[-1])

    prog = [int(ele) for ele in lines[4].strip().split()[1].split(",")]

instruction_pointer = 0


def combo_op(op: int):
    if op <= 3:
        return op
    combo = {
        4: reg_a,
        5: reg_b,
        6: reg_c
    }
    return combo[op]


def adv(op: int):
    global reg_a
    reg_a = reg_a // (2**combo_op(op))
    return None, 2


def bxl(op: int):
    global reg_b
    reg_b = reg_b ^ op
    return None, 2


def bst(op: int):
    global reg_b
    reg_b = combo_op(op) % 8
    return None, 2


def jnz(op: int):
    global instruction_pointer
    if reg_a != 0:
        instruction_pointer = op
        return None, 0
    return None, 2


def bxc(op: int):
    global reg_b
    reg_b = reg_b ^ reg_c
    return None, 2


def out(op: int):
    c = combo_op(op) % 8
    return c, 2


def bdv(op: int):
    global reg_b
    reg_b = reg_a // (2**combo_op(op))
    return None, 2


def cdv(op: int):
    global reg_c
    reg_c = reg_a // (2**combo_op(op))
    return None, 2


ops = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]


def run():
    global instruction_pointer
    halted = False
    all_output = []
    while not halted:
        # print(instruction_pointer)
        operator = prog[instruction_pointer]
        operand = prog[instruction_pointer + 1]
        operator = ops[operator]
        output, instruction_step = operator(operand)
        if not output is None:
            all_output.append(output)
        instruction_pointer += instruction_step
        halted = instruction_pointer >= len(prog)
    return all_output


all_output = run()
res1 = ",".join(str(ele) for ele in all_output)
print(f'{res1=}')


# p2
reg_a = 117440
reg_b = 0
reg_c = 0
instruction_pointer = 0
# print(run())

print(prog[::2])

# out: 0
# 


