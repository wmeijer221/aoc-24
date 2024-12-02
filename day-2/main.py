
with open("./day-2/input.txt", "r") as input_file:
    data = input_file.readlines()
    entries = []
    for line in data:
        line_ele = [int(ele) for ele in line.strip().split()]
        entries.append(line_ele)


count_safe_p1 = 0
count_safe_p2 = 0


def is_safe(cur_ele, next_ele, cur_sign):
    if cur_ele == next_ele or (abs(next_ele - cur_ele) > 3):
        return False, cur_sign

    my_sign = (next_ele - cur_ele) < 0

    if cur_sign is None:
        return True, my_sign

    if cur_sign != my_sign:
        return False, cur_sign
    
    return True, cur_sign


for entry in entries:
    sign = None
    entry_iterator = enumerate(entry[:-1])
    safe_p1 = True
    safe_p2 = True
    safe_p2_limit = False
    for idx, cur_ele in entry_iterator:
        next_ele = entry[idx + 1]

        safe_p1_ele, my_sign = is_safe(cur_ele, next_ele, sign)
        if sign is None:
            sign = my_sign
        safe_p1 = safe_p1 and safe_p1_ele

        safe_p2 = safe_p1 or (not safe_p1 and not safe_p2_limit)

        if not safe_p1 and not safe_p2_limit and idx < len(entry) - 2:
            safe_p2_a, cur_sign = is_safe(cur_ele, entry[idx+2], sign)
            if safe_p2_a:
                sign = cur_sign
                next(entry_iterator)
                continue
            safe_p2_b, cur_sign = is_safe(next_ele, entry[idx+2], sign)
            if safe_p2_b:
                sign = cur_sign
                next(entry_iterator)
                continue
            safe_p2 = False
            break

    if safe_p1:
        count_safe_p1 += 1

    if safe_p2:
        count_safe_p2 += 1


print(f'{count_safe_p1=}')
print(f'{count_safe_p2=}')
