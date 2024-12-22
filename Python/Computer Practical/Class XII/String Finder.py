uInput = input('Enter Some Text:- ')
uStr = input('Enter The Char Or String To Find:- ')


def findString():
    if uStr in uInput:
        posStr = uInput.index(uStr)
        if len(uStr) > 1:
            print(f'String Found At {posStr}')
        else:
            print(f'Char Found At {posStr}')
    else:
        print('Given String Not Found')


findString()
