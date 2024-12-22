from string import *

char = input('Enter The Character :- ')


def findChar(character):
    while len(character) > 1:
        character = input('PLease Enter A Single Character Only :- ')

    if character in printable[-6:-3]:
        return 'Whitespace'
    elif character in ascii_lowercase:
        return 'LowerCase Alphabet'
    elif character in ascii_uppercase:
        return 'UpperCase Alphabet'
    elif character in digits:
        return 'Digits'
    else:
        return 'Special Symbol'


print(findChar(char))
