

q = ['a', 'b', 'c', 'd']

for i, e in enumerate(q):
    for e2 in q[i+1:]:
        print((e, e2))
