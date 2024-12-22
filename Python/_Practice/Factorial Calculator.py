def fact(num):
    if num > 1:
        output = num * fact(num-1)
        return output
    elif num == 0:
        return 1
    else:
        output = num * 1
        return output


print(fact(int(input())))
