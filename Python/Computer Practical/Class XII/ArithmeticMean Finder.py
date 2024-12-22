numList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
print('Use [] At Start And End')
uList = list(eval(input('Enter The List :- ')))
totalElements = len(uList)


def arithmeticMean(List):
    sumOfNum = 0
    for i in List:
        if type(i) != int:
            List = list(eval(input('Enter The List Again :- ')))

    for num in List:
        sumOfNum += num

    Mean = sumOfNum / totalElements
    return Mean


print(arithmeticMean(uList))
