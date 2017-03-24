import itertools
import functools

def getAllCombinations(object_list, n):
    roll = []
    for i in itertools.product([str(j) for j in range(0, n)], repeat=4):
        roll.append(list(map(int, i)))
        #[int(c) for c in i])
    return roll

def solve(arr):
    array = getAllCombinations(range(len(arr)), 5)
    #print([str(i) for i in reversed(array)])
    for c in array:
        total = 0
        for i in range(len(arr)):
            if len(c) == len(arr):
                total += arr[i] ** c[i]

        if total == 2006:
            print(c)
            print(total)
            print(functools.reduce(lambda a,b: a+b, c))
            print("found it")

solve([5,6,7,11])

