from tkinter import messagebox as mb, Tk

file = 'Student.txt'

# ====GUI Window Removal====
Tk().geometry('0x0+1000+1000')


def studentRecord():
    f = open(file, 'a')
    while True:
        rollNum = input('Enter The Student Roll Number:- ')
        while not rollNum.isdigit():
            rollNum = input('Enter Roll Number Only In Numerals:- ')
        name = input('Enter The Student Name:- ')
        address = input('Enter The Address:- ')
        while rollNum == '':
            rollNum = int(input('Enter The Student Roll Number:- '))

        while name == '':
            name = input('Enter The Student Name:- ')

        while address == '':
            address = input('Enter The Address:- ')

        choice = input('Wish To Continue(Y/n):- ')
        recLst = f"Roll Number:- {rollNum},Name:- {name}|Address:- {address}\n"
        f.write(recLst)
        if choice.lower() == 'n':
            break


def studentReadData(fullRead=True):
    f = open(file, 'r')
    recLst = f.readlines()
    reqLst = []
    for i in recLst:
        tmpLst = [i.split(',', 1)[0]] + i.split(',', 1)[1].split('|')
        reqLst.append(tmpLst)

    for i in reqLst:
        if fullRead:
            print(i[0])
            print(i[1])
            print(i[2])

    if not fullRead:
        x = 0
        gRollNum = input('Enter The Roll Number To Search:- ')
        for i in reqLst:
            if gRollNum in i[0].split(' '):
                print(i[0])
                print(i[1])
                print(i[2])
                x = 1
                continue
        if x == 0:
            mb.showerror('Error', 'Roll Number Not Found!')


def studentSearch():
    studentReadData(False)


mb.showinfo('Operations Available',
            '''Keys To Use For
Inserting :- I
Reading :- R
Searching :- S
Exiting :- X''')
choiceI = input('Enter The Option:- ')

while True:
    choices = ('r', 'i', 's', 'x', 'y')
    if choiceI.lower() == 'r':
        studentReadData()
        choiceI = input('Wish To Continue(Y/x):- ')
    elif choiceI.lower() == 'i':
        studentRecord()
        choiceI = input('Wish To Continue(Y/x):- ')
    elif choiceI.lower() == 's':
        studentSearch()
        choiceI = input('Wish To Continue(Y/x):- ')
    elif choiceI.lower() == 'y':
        choiceI = input('Enter The Option(R/I/S/X):- ')
    elif choiceI.lower() == 'x':
        break
    while choiceI not in choices:
        choiceI = input('Enter The Correct Option(R/I/S/X):- ')
