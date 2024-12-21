
from functools import cache
from typing import Tuple
from collections.abc import Sequence
import math
with open("./day-21/input.txt", 'r') as input_file:
    codes = [tuple(line.strip()) for line in input_file]

print(codes)


keypad1 = (
    ('7', '8', '9'),
    ('4', '5', '6'),
    ('1', '2', '3'),
    (None, '0', 'A'))
keypad2 = (
    (None, '^', 'A'),
    ('<', 'v', '>'))


def create_key_to_coord_mapping(keypad):
    mapping = {}
    for y, row in enumerate(keypad):
        for x, ele in enumerate(row):
            mapping[ele] = (x, y)
    return mapping


keypad1_mapping = create_key_to_coord_mapping(keypad1)
keypad2_mapping = create_key_to_coord_mapping(keypad2)

delta_to_keypad2 = {(-1, 0): "<", (1, 0): ">", (0, -1): "^", (0, 1): "v"}

keypad1_pos = (2, 3)
keypad2_pos = (2, 0)

nbs = [[-1, 0], [0, 1], [1, 0], [0, -1]]


SinglePathAlternatives = Sequence[Sequence[Tuple[int]]]


@cache
def shortest_path(start, end, keypad) -> SinglePathAlternatives:
    to_visit = set()
    start = (start[0], start[1])
    end = (end[0], end[1])
    to_visit.add((start, 0, (start,)))
    best_cost = math.inf
    best_paths = list()
    while len(to_visit) > 0:
        my_pos, my_cost, my_path = to_visit.pop()
        if my_pos == end:
            if my_cost < best_cost:
                best_cost = my_cost
                best_paths = list()
            if my_cost <= best_cost:
                best_paths.append(my_path)
            continue
        my_cost = my_cost + 1
        for nb in nbs:
            nb_pos = (my_pos[0] + nb[0], my_pos[1] + nb[1])
            if nb_pos in my_path:
                continue
            if nb_pos[0] < 0 or nb_pos[0] >= len(keypad[0]) or nb_pos[1] < 0 or nb_pos[1] >= len(keypad):
                continue
            if keypad[nb_pos[1]][nb_pos[0]] is None:
                continue
            next_path = (*my_path, nb_pos)
            to_visit.add((nb_pos, my_cost, next_path))
    return best_paths


def find_shortest_paths(code: Sequence[str], start_pos, keypad, keypad_mapping):
    current_pos = start_pos
    chunks = list()
    for ele in code:
        target = keypad_mapping[ele]
        p = shortest_path(tuple(current_pos), tuple(target), keypad)
        chunks.append(p)
        current_pos = target
    return chunks


def to_keys(seq, keypad_mapping):
    inp = list()
    for i in range(len(seq) - 1):
        delta = (seq[i+1][0] - seq[i][0], seq[i+1][1] - seq[i][1])
        key = keypad_mapping[delta]
        inp.append(key)
    inp.append("A")
    return inp

# Given an input, figure out the different shortest paths to fill out that code.
# Translate the paths into keypresses of the preceding keypad
# Translate each of these keypresses into the shortest paths to fill out those codes.
# Translate each of these shortest paths to the keypresses filled into the preceding keypad.


@cache
def get_input(code: Tuple[str], use_keypad1: bool, max_depth: int, depth: int):
    start_pos = keypad1_pos if use_keypad1 else keypad2_pos
    keypad = keypad1 if use_keypad1 else keypad2
    keypad_mapping = keypad1_mapping if use_keypad1 else keypad2_mapping
    shortest_paths = find_shortest_paths(
        code, start_pos, keypad, keypad_mapping)
    if depth < max_depth:
        input = 0
        for path_chunk_alts in shortest_paths:
            best_chunk_input = None
            for path_alt in path_chunk_alts:
                alt_keypresses = to_keys(
                    path_alt, delta_to_keypad2)
                alt_keypresses = tuple(alt_keypresses)
                alt_input = get_input(
                    alt_keypresses, False, max_depth, depth + 1)
                if best_chunk_input is None or alt_input < best_chunk_input:
                    best_chunk_input = alt_input
            input += best_chunk_input
    else:
        alt_keypresses = [to_keys(path_chunk_alts[0], delta_to_keypad2)
                          for path_chunk_alts in shortest_paths]
        alt_keypresses = ["".join(ele) for ele in alt_keypresses]
        input = "".join(alt_keypresses)
        input = len(input)
    return input


total1 = 0
for code in codes:
    inp_len = get_input(code, True, 2, 0)
    # inp_len = len(inp)
    num = int("".join(code[:-1]))
    complexity = num * inp_len
    total1 += complexity

print(f'{total1=}')

total2 = 0
for code in codes:
    inp_len = get_input(code, True, 25, 0)
    # inp_len = len(inp)
    num = int("".join(code[:-1]))
    complexity = num * inp_len
    total2 += complexity

print(f'{total2=}')
