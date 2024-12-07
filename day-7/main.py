with open("./day-7/input.txt", "r") as input_file:
    data = [line.strip().split(": ") for line in input_file.readlines()]
    data = [(int(ele[0]), [int(term) for term in ele[1].split()]) for ele in data]


def can_calculate(y, leftX, rightX) -> bool:
    ele = rightX[0]
    rightX = rightX[1:]

    leftXAdd = ele + leftX
    leftXMult = ele * leftX

    if len(rightX) == 0:
        return leftXAdd == y or leftXMult == y

    can_calculate_add = leftXAdd <= y and can_calculate(y, leftXAdd, rightX)
    can_calculate_mult = leftXMult <= y and can_calculate(y, leftXMult, rightX)

    return can_calculate_add or can_calculate_mult


def can_calculate2(y, leftX, rightX) -> bool:
    ele = rightX[0]
    rightX = rightX[1:]

    leftXAdd = ele + leftX
    leftXMult = ele * leftX
    leftXConc = int(str(leftX) + str(ele))

    if len(rightX) == 0:
        return leftXAdd == y or leftXMult == y or leftXConc == y

    can_calculate_add = leftXAdd <= y and can_calculate2(y, leftXAdd, rightX)
    can_calculate_mult = leftXMult <= y and can_calculate2(y, leftXMult, rightX)
    can_calculate_conc = leftXConc <= y and can_calculate2(y, leftXConc, rightX)

    return can_calculate_add or can_calculate_mult or can_calculate_conc


count1 = 0
count2 = 0
for y, X in data:
    if can_calculate(y, 0, X):
        count1 += y
        count2 += y
    elif can_calculate2(y, 0, X):
        count2 += y


# 4019885351117 is too low
# 4122618559853 is right
print(f"{count1=}")

# 118003791566582 is too low
# 227615740238334 is right
print(f"{count2=}")
