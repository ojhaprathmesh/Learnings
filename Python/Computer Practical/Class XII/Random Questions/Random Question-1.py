def editString(uString):
    uString = list(uString)
    for i in range(len(uString)):
        if uString[i] == uString[i-1]:
            uString[i] = '*'

    return ''.join(uString)


print(editString('AAijkllMMnop'))
