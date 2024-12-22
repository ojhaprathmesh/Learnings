from random import randint, choice
import string

passLen = int(input("Enter Length Of Password:- "))
keyList = list(string.printable[:94])

num = keyList[:10]
upper = keyList[10:36]
lower = keyList[36:62]
special = keyList[62:]

keyDict = {1: upper, 2: lower, 3: num, 4: special}

outPassList = []

while len(outPassList) != passLen:
    outPassList.append(choice(keyDict[randint(1, 4)]))

print(''.join(outPassList))
