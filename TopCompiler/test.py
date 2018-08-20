import itertools
from time import time

def find(n, x):
    x *= n
    found = []

    for c in range(n, 2*n+1):
        a = c / n
        for d in range(2*n, x):
            b = d / n
            if a+b == a*b:
                found.append((a, b))

    #arr = [(a+b) for (a,b) in found]
    #print(arr)
    #print(", ".join(["%.2f" % (b+1 - b) for ((a,b),result) in zip(found, arr)]))
    return found


def optFind(n):
    n = 10 ** n
    found = []
    for x in range(n+1, 2*n+1):
        x /= n
        y = x/(x-1)

        found.append((x, y))

    (a,b) = found[0]

    return found

"""
a <= 2
b >= 2


2 2
"""