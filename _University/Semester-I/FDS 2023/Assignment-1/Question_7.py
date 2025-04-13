string = "hello world and practice makes perfect and hello world again"
tempList = string.split()
reqList = []
for word in tempList:
    if word not in reqList:
        reqList.append(word)
reqList.sort()

for i in reqList:
    print(i, end=' ')
