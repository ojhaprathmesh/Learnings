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
    elif character in punctuation:
        return 'Punctuation Symbol'
    else:
        return 'Special Symbol'


while True:
    print(findChar(char))
    choice = input('Want To Continue(Y/n):- ')
    if choice.lower() == 'n':
        break
    char = input('Enter The Character :- ')
