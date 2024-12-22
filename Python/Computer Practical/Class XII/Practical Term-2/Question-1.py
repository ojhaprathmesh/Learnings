stack = []


def isEmpty(Stack):
    if not Stack:
        return True
    else:
        return False


def pushRecord():
    while True:
        bookNum = input('Enter The Book Number :- ')
        bookName = input('Enter The Name Of Book :- ')
        stack.append((bookNum, bookName))
        choice = input('Want To Continue(Y/n):- ')
        
        if choice.lower() == 'n':
            break
        elif choice.lower() == 'y':
            pass
        while choice.lower() != 'n' and choice.lower() != 'y':
            choice = input('Want To Continue(Y/n):- ')


def displayRecord():
    if not isEmpty(stack):
        for record in stack:
            print(f"Book Number:- {record[0]}")
            print(f"Book Name:- {record[1]}")
    else:
        print('Empty Stack')


while True:
    userChoice = input('Enter The Operation(Push-P/Display-D/Exit-X):- ')
    if userChoice.lower() == "p":
        pushRecord()
    elif userChoice.lower() == "d":
        displayRecord()
    elif userChoice.lower() == "x":
        break
    else:
        userChoice = input('Please Enter The Correct Operation(Push-P/Display-D/Exit-X):- ')

