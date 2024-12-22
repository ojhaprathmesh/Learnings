uList = list(eval(input('Enter The Numeric List:- ')))
finLst = []  # Final List With Output


def shiftNeg():
    for i in uList:
        if i < 0:
            finLst.append(i)

    for i in uList:
        if i >= 0:
            finLst.append(i)


shiftNeg()
print(f'{uList}\033[1m-->\033[0m{finLst}')
