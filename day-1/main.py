
with open('./day-1/input.txt', 'r') as input_file:
    input = input_file.readlines()
    list_a = list()
    list_b = list()
    for line in input:
        a, b = line.strip().split()
        list_a.append(int(a))
        list_b.append(int(b))


list_a.sort()
list_b.sort()

sum = 0
for a, b in zip(list_a, list_b):
    sum += abs(a - b)

print(f'{sum=}')


count = dict()
for ele in list_b:
    if ele not in count:
        count[ele] = 0
    count[ele] += 1

sum2 = 0
for ele in list_a:
    if ele not in count:
        continue
    sum2 += ele * count[ele]

print(f'{sum2=}')
