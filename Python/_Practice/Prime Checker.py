num = 1
while num <= 100:
    output = True
    for i in range(1, num):
        if num % i == 0 and 1 not in [i, num]:
            output = False
    if output:
        print(num)
    num += 1


"""
2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 73 79 83 89 97
"""