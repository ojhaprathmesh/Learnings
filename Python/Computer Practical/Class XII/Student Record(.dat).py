from pickle import *
from tkinter import messagebox as mb, Tk

# ====GUI Window Removal====
Tk().geometry('0x0+1000+1000')


# ====Commands For Operations On Student Record File====
def readRec():
    try:
        f = open('Student Record.dat', 'rb')
        recLst = load(f)
        f.close()
        print('\033[1m==== Available Records ====\033[0m')

        for i in recLst:
            if str(i) == '[]':
                continue
            print(f"\033[1mRoll Number:- \033[1;34m{i[0]}\033[0m")
            print(f"\033[1mStudent Name:- \033[1;34m{i[1]}\033[0m")
            print(f"\033[1mMarks:- \033[1;34m{i[2]}\033[0m")

    except EOFError:
        print('\033[1m==== No Records Available ====\033[0m')
        mb.showerror('Error', 'No Records Available!')


def insertRec():
    try:
        f = open('Student Record.dat', 'rb')
        try:
            recLst = load(f)

        except EOFError:
            recLst = []
        f.close()
        if str(recLst) == '[]':
            recLst.append([])

        mb.showinfo('Information', f'Please Enter The Roll Number And Marks In Numerals Only.')
        while True:
            x = 0
            rollNum = int(input('Enter The Roll Number:- '))
            name = input('Enter The Student Name:- ')
            marks = int(input('Enter The Marks:- '))
            record = [rollNum, name, marks]
            for i in range(len(recLst)):
                if str(recLst[i]) == '[]':
                    recLst[i] = record

                if str(recLst[i][0]) == str(record[0]):
                    mb.showwarning(f'Roll Number {rollNum} Already Exists!',
                                   'You Are Going To Overwrite Existing Data!')
                    choice = input('Wish To Overwrite The Existing Data(Y/n)? :- ')
                    x += 1
                    if choice.lower() == 'y':
                        recLst[i] = record

                if len(recLst) - 1 == i and x == 0:
                    recLst.append(record)

            choice = input('Wish To Enter More Records(Y/n)? :- ')
            if choice.lower() == 'n':
                break

        f = open('Student Record.dat', 'wb')
        dump(recLst, f)
        f.close()

    except Exception as e:
        mb.showerror('Error', f'{e}!')


def updateRec():
    try:
        f = open('Student Record.dat', 'rb')
        recLst = load(f)
        f.close()
        while True:
            x = 0
            rollNum = input('Enter The Roll No. To be Updated:- ')
            for i in range(len(recLst)):
                if str(recLst[i][0]) == rollNum:
                    recLst[i][1] = input('Enter The Student Name:- ')
                    recLst[i][2] = int(input('Enter The Marks:- '))
                    x = 1

            if x == 0:
                print('\033[1mNo Records Found!\033[0m')

            choice = input('Wish To Update Other Records(Y/n)? :- ')
            if choice.lower() == 'n':
                break

        f = open('Student Record.dat', 'wb')
        dump(recLst, f)
        f.close()
        print('\033[1m==== Records Updated ====\033[0m')

    except EOFError:
        mb.showerror('Error', 'Record Not Found!')


def searchRec():
    try:
        f = open('Student Record.dat', 'rb')
        recLst = load(f)
        while True:
            choice = input('Search By Name, RollNum Or Marks(N/R/M):- ')
            if choice.lower() == 'n':
                x = 0
                sName = input('Enter The Student Name:- ')
                for i in recLst:
                    if str(i) == '[]':
                        continue

                    if i[1] == sName:
                        print(f"\033[1mRoll Number:- \033[1;34m{i[0]}\033[0m")
                        print(f"\033[1mStudent Name:- \033[1;34m{i[1]}\033[0m")
                        print(f"\033[1mMarks:- \033[1;34m{i[2]}\033[0m")
                        x += 1

                if x == 0:
                    mb.showerror('Error', 'No Records Found!')

                choice = input('Wish To Continue(Y/n):- ')
                if choice.lower() == 'n':
                    break

            elif choice.lower() == 'r':
                x = 0
                sRollNum = int(input('Enter The Roll Num:- '))
                for i in recLst:
                    if str(i) == '[]':
                        continue

                    if i[0] == sRollNum:
                        print(f"\033[1mRoll Number:- \033[1;34m{i[0]}\033[0m")
                        print(f"\033[1mStudent Name:- \033[1;34m{i[1]}\033[0m")
                        print(f"\033[1mMarks:- \033[1;34m{i[2]}\033[0m")
                        x += 1
                if x == 0:
                    mb.showerror('Error', 'No Records Found!')

                choice = input('Wish To Continue(Y/n):- ')
                if choice.lower() == 'n':
                    break

            elif choice.lower() == 'm':
                x = 0
                sMarks = input('Enter The Student Marks:- ')
                for i in recLst:
                    if str(i) == '[]':
                        continue

                    if i[2] == sMarks:
                        print(f"\033[1mRoll Number:- \033[1;34m{i[0]}\033[0m")
                        print(f"\033[1mStudent Name:- \033[1;34m{i[1]}\033[0m")
                        print(f"\033[1mMarks:- \033[1;34m{i[2]}\033[0m")
                        x += 1
                if x == 0:
                    mb.showerror('Error', 'No Records Found!')

                choice = input('Wish To Continue(Y/n):- ')
                if choice.lower() == 'n':
                    break

            else:
                choice = input('You Entered A Wrong Choice! Select (N/R/M) or Exit(X):- ')

            if choice.lower() == 'x':
                break

    except Exception as e:
        mb.showerror('Error', f'{e}!')


def delRec():
    try:
        f = open('Student Record.dat', 'rb')
        record = load(f)
        f.close()
        while True:
            x = 0
            drollNum = input('Enter The Roll Number To Be Deleted:- ')
            for i in range(len(record)):
                if str(record[i][0]) == drollNum:
                    del record[i]
                    x += 1
                    break

                if x == 0:
                    mb.showerror('Error', 'No Records Found!')

            choice = input('Want To Continue(Y/n)? :- ')
            if choice.lower() == 'n':
                break

        f = open('Student Record.dat', 'wb')
        dump(record, f)
        f.close()

    except Exception as e:
        mb.showerror('Error', f'{e}!')


mb.showinfo('Operations Available',
            '''Keys To Use For
Reading :- R
Inserting :- I
Updating :- U
Searching :- S
Deleting :- D
Exiting :- X''')
choiceI = input('Enter The Option:- ')

while True:
    choices = ('r', 'i', 'u', 's', 'd', 'x')
    if choiceI.lower() == 'r':
        readRec()
        choiceI = input('Wish To Continue:- ')
    elif choiceI.lower() == 'i':
        insertRec()
        choiceI = input('Wish To Continue:- ')
    elif choiceI.lower() == 'u':
        updateRec()
        choiceI = input('Wish To Continue:- ')
    elif choiceI.lower() == 's':
        searchRec()
        choiceI = input('Wish To Continue:- ')
    elif choiceI.lower() == 'd':
        delRec()
        choiceI = input('Wish To Continue:- ')
    elif choiceI.lower() == 'x':
        break
    while choiceI not in choices:
        choiceI = input('Enter The Correct Option(R/I/U/S/D/X):- ')
