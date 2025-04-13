from math import pi


def square_area(side):
    return side ** 2


def circle_area(radius):
    return pi * radius ** 2


length = 4
rad = 7

print(f"Area Of Square Of Side {length}: {square_area(length)}")
print(f"Area Of Circle Of Radius {rad}: {round(circle_area(rad), 2)}")
