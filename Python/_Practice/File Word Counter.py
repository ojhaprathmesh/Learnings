import string

fileName = input("Enter A Valid File Path:- ")


def makeDict(listInput):
    listOutput = []
    for i in listInput:
        if i[-1] in string.punctuation:
            listOutput.append(i[:-1])
        elif i not in string.whitespace:
            listOutput.append(i)

    wordDict = {}
    for i in listOutput:
        repeat = 0
        for j in listOutput:
            if i == j:
                repeat += 1
                wordDict[i] = repeat

    return wordDict


try:
    with open(f"{fileName}") as f:
        text = f.read()
        textList = text.split(' ')
        mainDict = makeDict(textList)
        for data in mainDict:
            print(data, mainDict[data])
except FileNotFoundError:
    print("The File Does Not Exists!")
