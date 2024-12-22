try:
    uNum1 = int(input('Enter First Number(a):- '))
    uNum2 = int(input('Enter Second Number(b):- '))
    operation = input("Enter Operation\n'+' For Addition\n'-' For Subtraction\n"
                                        "'x' or '*' For Multiplication\n'/' For Division :- ")

    if operation == '+':
        result = uNum1 + uNum2
        print(result)

    elif operation == '-':
        while True:
            choice = input('For a-b, Enter 1\nFor b-a, Enter 2\nEnter 3 To Exit: ')
            if choice == '1':
                result = uNum1 - uNum2
                print(result)
            elif choice == '2':
                result = uNum2 - uNum1
                print(result)
            elif choice == '3':
                break

    elif operation in ('x', '*'):
        result = uNum1 * uNum2
        print(result)

    elif operation == '/':
        while True:
            choice = input('For a/b, Enter 1\nFor b/a, Enter 2\nEnter 3 To Exit: ')
            if choice == '1':
                if uNum2 != 0:
                    result = uNum1 / uNum2
                    print(result)
                else:
                    print('Not Defined')
            elif choice == '2':
                if uNum1 != 0:
                    result = uNum2 / uNum1
                    print(result)
                else:
                    print('Not Defined')
            elif choice == '3':
                break

except Exception:
    print(f'Provided Input Is Not An Integer')
