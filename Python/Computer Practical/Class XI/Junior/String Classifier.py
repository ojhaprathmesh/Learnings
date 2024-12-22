String = input('Enter A String: ')

if len(String) == 1:
    if String.isspace():
        print('Whitespace')
    elif String.isdigit():
        print('Digit')
    elif String.islower():
        print('LowerCase Alphabet')
    elif String.isupper():
        print('UpperCase Alphabet')
    elif String.isprintable():
        print('Special Symbol')
else:
    if String[0].isspace():
        if String.isspace():
            print('Multiple Whitespaces')
        else:
            print('Arbitrary String With Space At 0')
    else:
        if String.isdigit():
            print('Numerals')
        elif String.istitle():
            if String.isalpha():
                print('Arbitrary String With Capital At 0')
            elif String.isalnum():
                print('Arbitrary String With Capital At 0 And Numeral(s)')
        elif String.isalpha():
            print('Arbitrary String')
        elif String.isalnum():
            print('Arbitrary String With Numeral(s)')
        elif String.isprintable():
            print('Arbitrary String With Special Symbols')
