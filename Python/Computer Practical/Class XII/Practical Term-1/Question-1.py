import csv

Labels = ['Username', 'Password']
File = open('UserId Record.csv', 'a+', newline='')

Writer = csv.writer(File)
Reader = csv.reader(File)
File.seek(0, 0)

for content in Reader:
    if content == Labels:
        break

    else:
        Writer.writerow(Labels)
        break


def insertRec():
    Entries = []
    while True:
        userName = input('Enter The Username:- ')
        password = input('Enter The Password:- ')

        Entries.append([userName, password])

        choice = input('Wish To Continue(Y/n):- ')
        if choice.lower() == 'n':
            Writer.writerows(Entries)
            break


def readRec():
    File.seek(0, 0)
    for record in Reader:
        if record != Labels:
            print(f'Username:- {record[0]}')
            print(f'Password:- {record[1]}')


def searchRec():
    while True:
        UserID = input('Enter The Username:- ')
        File.seek(0, 0)
        for record in Reader:
            if record[0] == UserID:
                print(f'Username:- {record[0]}')
                print(f'Password:- {record[1]}')
                break
        choice = input('Wish To Continue(Y/n):- ')
        if choice.lower() == 'n':
            break


print('To Read :- r\n'
      'To Insert :- i\n'
      'To Search :- s\n'
      'To Exit :- x')
while True:
    uChoice = input('Enter The Operation(r/i/s/x):- ')
    if uChoice.lower() == 'r':
        readRec()
    elif uChoice.lower() == 's':
        searchRec()
    elif uChoice.lower() == 'i':
        insertRec()
    elif uChoice.lower() == 'x':
        break
    else:
        print('\033[1;31;1mYou Entered A Wrong Choice!\033[0m')
