char = input('Enter A Character: ')

while len(char) > 1:
    char = input('Enter Single Character Only: ')

if char.isspace():
    print('Whitespace')
elif char.isdigit():
    print('Digit')
elif char.islower():
    print('LowerCase Alphabet')
elif char.isupper():
    print('UpperCase Alphabet')
elif char.isprintable():
    print('Special Symbol')

