
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

def entry_is_safe(entry: list):
    sign = None
    for idx, cur_ele in enumerate(entry[:-1]):
        next_ele = entry[idx + 1]
        safe, new_sign = is_safe(cur_ele,next_ele, sign)
        if sign is None:
            sign = new_sign
        if not safe:
            return False, idx
        
    return True, -1

for entry in entries:
    safe_p1, err_idx = entry_is_safe(entry)
    safe_p2 = True
    if not safe_p1:
        new_entry0 = [*entry[0:err_idx - 1], *entry[err_idx:]]
        new_entry1 = [*entry[0:err_idx], *entry[err_idx + 1:]]
        new_entry2 = [*entry[0:err_idx + 1], *entry[err_idx + 2:]]
        new_entry0_safe, _ = entry_is_safe(new_entry0)
        new_entry1_safe, _ = entry_is_safe(new_entry1)
        new_entry2_safe, _ = entry_is_safe(new_entry2)
        safe_p2 = new_entry0_safe or new_entry1_safe or new_entry2_safe

    if safe_p1:
        count_safe_p1 += 1
    if safe_p2:
        count_safe_p2 += 1

    print(entry, safe_p1, safe_p2)


print(f'{count_safe_p1=}')
print(f'{count_safe_p2=}')
