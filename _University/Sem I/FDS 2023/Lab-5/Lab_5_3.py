def celsius2fahrenheit(degree):
    return degree * 9 / 5 + 32


def fahrenheit2celsius(degree):
    return (degree - 32) * 5 / 9


print(celsius2fahrenheit(100))
print(fahrenheit2celsius(212))
