
import math
import random
with open("./day-17/test-input2.txt", 'r') as input_data:
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



# reg_a = 117440
# reg_b = 0
# reg_c = 0
# instruction_pointer = 0
# print(bin(reg_a))
# print(oct(reg_a))
# my_res = run()
# print(my_res)



# n = 100
# l = 15


# def get_rnd_ele():
#     return random.randint(8**l, 8**l + 8**(l-1))


# population = [get_rnd_ele() for _ in range(n)]
# for _ in range(2000):
#     scores = []
#     for ele in population:
#         reg_a = ele
#         reg_b = 0
#         reg_c = 0
#         instruction_pointer = 0
#         my_run = run()
#         score = sum(1 if a == b else 0 for a, b in zip(my_run, prog))
#         scores.append((ele, score))
#     scores = sorted(scores, key=lambda x: -x[1])
#     scores = scores[:n//2]
#     print(scores[0:5])
#     population = [score[0] for score in scores]
#     random.shuffle(population)
#     mask_len = 46
#     mask_seg_len = mask_len // 2
#     mask_a = int("1" * mask_seg_len + "0" * mask_seg_len, 2)
#     mask_b = int("0" * mask_seg_len + "1" * mask_seg_len, 2)

#     new_population = []
#     for i in range(len(population) // 2):
#         j = i * 2
#         k = j + 1

#         a = population[j] & mask_a
#         b = population[k] & mask_b
#         c = a + b
#         cbin = bin(c)[2:]
#         idx = random.randint(0, len(cbin) - 1)
#         for _ in range(5):
#             cbin = cbin[:idx] + ("1" if cbin[idx]
#                                  == '0' else '1') + cbin[idx+1:]
#         c = int(cbin, 2)

#         d = population[k] & mask_a
#         e = population[j] & mask_b
#         f = d + e
#         fbin = bin(f)[2:]
#         idx = random.randint(0, len(fbin) - 1)
#         for _ in range(5):
#             fbin = fbin[:idx] + ("1" if fbin[idx] ==
#                                  '0' else '1') + fbin[idx+1:]
#         f = int(fbin, 2)

#         new_population.append(c)
#         new_population.append(f)

#     print(new_population)
#     population = new_population


# # p2
# l = 15
# # reg_a = 8**l
# # reg_a += 8**13 * 5
# # reg_a += 6
# # # for i in range(8):
# # # print(i)
# # # reg_a = 8**l + 8**13 + i
# # # for i in range(l-1):
# # # print(i)
# # # reg_a = 8**l + 8**i
# # # for j in range(l-1):
# # #     reg_a = reg_a + 8**j


# # # # reg_a += 8**(l-1)
# # # reg_a += 8 ** (l-2)
# # # reg_a += 8 ** (l-14)
# # # reg_a += 6

# # reg_b = 0
# # reg_c = 0
# # instruction_pointer = 0
# # res = run()
# # print(len(res))
# # print(res)
# # print()

# l = 15
# base_reg_a = 8**l
# instruction_pointer = 0
# reg_a = base_reg_a
# reg_b = 0
# reg_c = 0


# previous = run()
# for _ in range(2):
#     for i in range(l):
#         k = l - i - 1
#         f = 8**i
#         for j in range(8):
#             q = f * j
#             reg_a = base_reg_a + q
#             instruction_pointer = 0
#             reg_b = 0
#             reg_c = 0
#             my_run = run()
#             # print(my_run)
#             # print(prog)
#             my_ele = my_run[i]
#             targ_ele = prog[i]
#             print(i, my_run)
#             if my_ele == targ_ele:
#                 base_reg_a = base_reg_a + q
#                 print(f'{base_reg_a=}')
#                 break
#             # print()
#     reg_a = base_reg_a
#     instruction_pointer = 0
#     reg_b = 0
#     reg_c = 0
#     my_run = run()
#     print(my_run)
#     print(prog)
#     done = all(a == b for a, b in zip(my_run, prog))
#     if done:
#         break
