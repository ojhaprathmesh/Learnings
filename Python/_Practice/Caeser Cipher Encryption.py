strInp = input("Enter A String:- ")
shift = int(input("Enter The Shift:- "))

outList = []

for i in strInp:
    outList.append(chr(int(ord(i)) + shift))

strOut = ''.join(outList)

print(strOut)
