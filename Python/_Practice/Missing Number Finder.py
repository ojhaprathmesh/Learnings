inpArray = eval(input("Enter An Array. Make Sure To Open And Close With []:- "))
for i in range(inpArray[0], inpArray[-1]):
    if i not in inpArray:
        print(i)
