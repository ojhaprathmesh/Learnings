from math import acos, degrees

sideA = input("Enter Side 1: ")
sideB = input("Enter Side 2: ")
sideC = input("Enter Side 3: ")

while not sideA.isdigit():
    sideA = input("Enter A Correct Choice:- ")
a = int(sideA)

while not sideB.isdigit():
    sideB = input("Enter A Correct Choice:- ")
b = int(sideB)

while not sideC.isdigit():
    sideC = input("Enter A Correct Choice:- ")
c = int(sideC)


def find_angle(side1, side2, side3):
    # Convert degrees to radians for the final result
    return round(degrees(acos((side1 ** 2 + side2 ** 2 - side3 ** 2) / (2 * side1 * side2))),5)  # This statement executes the cosine formula and converts the radian output to degree output


print()  # Just to provide separation
print(f"Angle b/w Side-1 and Side-2 is {find_angle(a, b, c)}")
print(f"Angle b/w Side-2 and Side-3 is {find_angle(b, c, a)}")
print(f"Angle b/w Side-1 and Side-3 is {find_angle(c, a, b)}")
