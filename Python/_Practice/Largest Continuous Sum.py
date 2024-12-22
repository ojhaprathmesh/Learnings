array = eval(input("Enter A List Of Integers:- "))


def makeSubArrays(inpList):
    tempList = []
    size = len(inpList)
    for i in range(size, 0, -1):
        iteration = size - i + 1
        sliceSize = size - iteration + 1
        for j in range(iteration):
            tempList.append(inpList[0 + j:sliceSize + j])

    print(tempList)
    return tempList


def calcSubArraysSum(inpList):
    tempDict = {}
    for item in inpList:
        tempDict[inpList.index(item)] = [sum(item), item]
    return tempDict


def findLargestSum(inpDict):
    tempList = [[], []]
    for key in inpDict.keys():
        tempList[0].append(inpDict[key][0])
        tempList[1].append(inpDict[key][1])
    largestNum = max(tempList[0])
    reqIndex = tempList[0].index(largestNum)
    result = tempList[1][reqIndex]
    return result, largestNum


subArrayList = makeSubArrays(array)
subArrayDict = calcSubArraysSum(subArrayList)
print(findLargestSum(subArrayDict))
