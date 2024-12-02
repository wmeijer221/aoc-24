


x = [1,2,3, 4]
y = x[0:0]

print(y)


idx = 1

y = [*x[0:idx], *x[idx+1:]]
print(y)



y = x[-1:0]
print(y)

y = x[2:10]
print(y)


print(x[:-1])