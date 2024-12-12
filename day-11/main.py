from wmutils.collections.safe_dict import SafeDict


with open('./day-11/input.txt', 'r') as input_file:
    old_data = [ele for ele in input_file.read().strip().split()]

# p1
data = old_data
for i in range(25):
    new = []
    for idx, ele in enumerate(data):
        if ele == "0":
            new.append("1")
        elif len(ele) % 2 == 0:
            new.append(str(int(ele[:len(ele)//2])))
            new.append(str(int(ele[len(ele)//2:])))
        else:
            new.append(str(int(ele) * 2024))
    data = new

print(f"{len(data)=}")


# p2
data = SafeDict(default_value=0, initial_mapping={ele: 1 for ele in old_data})
for i in range(75):
    new = SafeDict(default_value=0)
    for idx, (ele, value) in enumerate(data.items()):
        if ele == "0":
            new["1"] += value
        elif len(ele) % 2 == 0:
            new[str(int(ele[:len(ele)//2]))] += value
            new[str(int(ele[len(ele)//2:]))] += value
        else:
            new[str(int(ele) * 2024)] += value
    data = new
    # print(new)

total2 = sum(data.values())
print(f'{total2=}')
