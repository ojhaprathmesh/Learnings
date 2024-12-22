from random import randint, shuffle
from string import printable


def nameGenerator(letters: list, size: int, upper: str = None):
    temp = letters
    shuffle(temp)
    for char in temp:
        if char.isupper():
            upper = char
            break

    letters.sort(reverse=True)
    letters = letters[:25]
    shuffle(letters)

    name = f'{upper}'
    for char in letters:
        if len(name) < n:
            name += char
        else:
            return name


n = randint(3, 18)  # Generates the size of name i.e. n
charList = [x for x in printable if x.isalpha()]  # Generates list of all alphabets

target = "Tushar"
count = 0
result = nameGenerator(charList, n)

while result != target:
    n = randint(3, 18)  # Generates the size of name i.e. n
    count += 1
    result = nameGenerator(charList, n)
    print(result)

print(result)

