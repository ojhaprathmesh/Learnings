sideA = input("Enter Side 1: ")
sideB = input("Enter Side 2: ")
sideC = input("Enter Side 3: ")

while not sideA.isdigit():
    sideA = input("Enter A Correct Choice:- ")
sideA = int(sideA)

while not sideB.isdigit():
    sideB = input("Enter A Correct Choice:- ")
sideB = int(sideB)

while not sideC.isdigit():
    sideC = input("Enter A Correct Choice:- ")
sideC = int(sideC)

sideList = [sideA, sideB, ]

run = True
for i in range(len(sideList)):
    if i == 2 and sideList[i]**2 == sideList[i-1]**2 + sideList[i-2]**2:
        run = False
    elif i != 2 and sideList[i] == sideList[i-1]*sideList[i+1]:
        run = False

if not run:
    print(f"\"{sideA, sideB, sideC}\" Is A Pythagorean Triplet")

else:
    print(f"\"{sideA, sideB, sideC}\" Is Not A Pythagorean Triplet")
