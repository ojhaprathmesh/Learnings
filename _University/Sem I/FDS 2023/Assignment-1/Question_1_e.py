def fact(num):
    if num in (0, 1):
        return 1
    else:
        return num * fact(num - 1)


print(fact(25))
