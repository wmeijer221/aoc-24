import math
with open("./day-22/input.txt", 'r') as input_file:
    start_prices = [int(line.strip()) for line in input_file]

from wmutils.collections.safe_dict import SafeDict

loops = 2000
total1 = 0
cumulative_price_after_pattern = SafeDict(default_value=0)
for price in start_prices:
    last_five_prices = ()
    change_pattern = ()
    price_after_pattern = dict()
    for _ in range(loops):
        if len(last_five_prices) == 5:
            last_five_prices = last_five_prices[1:]
            change_pattern = change_pattern[1:]

        price = ((price * 64) ^ price) % 16777216
        price = ((price // 32) ^ price) % 16777216
        price = ((price * 2048) ^ price) % 16777216

        adjusted_price = price % 10

        last_five_prices = (*last_five_prices, adjusted_price)
        if len(last_five_prices) >= 2:
            change = adjusted_price - last_five_prices[-2]
            change_pattern = (*change_pattern, change)

        if len(change_pattern) == 4:
            if change_pattern not in price_after_pattern:
                price_after_pattern[change_pattern] = adjusted_price

            # elif price_after_pattern[change_pattern] is None:
                # price_after_pattern[change_pattern] = price

    # print(price_after_pattern)
    for pattern, gained_price in price_after_pattern.items():
        # if gained_price is None:
        # continue
        cumulative_price_after_pattern[pattern] += gained_price

    total1 += price
print(f'{total1=}')


def dict_argmax(d):
    mx = -math.inf
    arg_mx = None
    for key, value in d.items():
        if value > mx:
            mx = value
            arg_mx = key
    return arg_mx


pattern = dict_argmax(cumulative_price_after_pattern)
total2 = cumulative_price_after_pattern[pattern]
# print(pattern)s
print(f'{total2=}')
