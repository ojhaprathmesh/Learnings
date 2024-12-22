import random
from string import printable
from datetime import datetime


def createCAPTCHA():
    iList = list(printable[:-6:])
    rList = ['"', "'", '+', ',', '.', '\\', '(', ')']
    length = random.randint(6, 10)
    captcha = ''
    for i in iList:
        if i in rList:
            iList.remove(i)

    del iList[iList.index('(')]
    for i in range(length):
        captcha += iList[random.randint(0, 86)]

    with open('CAPTCHA.txt', 'a') as f:
        if len(captcha) < 8:
            f.write(f'{captcha}\t\t\tGenerated On :- {datetime.now()}\n')
        else:
            f.write(f'{captcha}\t\tGenerated On :- {datetime.now()}\n')
        f.close()

    print(f'\033[3m\033[1m\n\n\t\t{captcha}\n\033[0m')


createCAPTCHA()
