from math import sqrt


def hypotenuse(b, p):

    h = round(sqrt(b ** 2 + p ** 2), 5)

    print(f"Hypotenuse Of Triangle With Base-{b} And Perpendicular-{p} Is {h}")
    return h


base = eval(input("Enter Base Length: "))
perpendicular = eval(input("Enter Perpendicular Length: "))

hypotenuse(base, perpendicular)
