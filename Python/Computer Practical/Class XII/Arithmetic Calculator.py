def calculation(Num1, Num2):
    operation = input("Enter Operation\n'+' For Addition\n'-' For Subtraction\n'x' or '*' For Multiplication\n'/' "
                      "For Division :- ")

    if operation == '+':
        result = Num1 + Num2
        return result
    elif operation == '-':
        while True:
            choice = input('For a-b, Enter 1\nFor b-a, Enter 2 :- ')
            if choice == '1':
                result = uNum1 - uNum2
                return result
            elif choice == '2':
                result = uNum2 - uNum1
                return result
            else:
                print('You Entered A Wrong Choice', end='')
    elif operation == 'x' or operation == '*':
        result = Num1 * Num2
        return result
    elif operation == '/':
        while True:
            choice = input('For a/b, Enter 1\nFor b/a, Enter 2 :- ')
            if choice == '1':
                if uNum2 != 0:
                    result = uNum1 / uNum2
                    return result
                else:
                    return '\033[1mNot Defined\033[0m'
            elif choice == '2':
                if uNum1 != 0:
                    result = uNum2 / uNum1
                    return result
                else:
                    return '\033[1mNot Defined\033[0m'
            else:
                print('You Entered A Wrong Choice')


try:
    uNum1 = int(input('Enter First Number(a):- '))
    uNum2 = int(input('Enter Second Number(b):- '))
    print(calculation(uNum1, uNum2))

except Exception as e:
    print(f'Provided Input Is Not An \033[1;31;1mInteger\033[0m')
    print(f'\033[1;31;1m{e}\033[0m')
