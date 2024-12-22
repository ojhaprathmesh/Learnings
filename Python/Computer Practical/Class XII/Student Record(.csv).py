import csv

Labels = ['Roll No.', 'Name', 'Marks']
File = open('Student Record.csv', 'r', newline='')
Reader = csv.reader(File)
e1 = "invalid literal for int() with base 10:"
e2 = "could not convert string to float:"

for row in Reader:
    if row[0] == Labels[0]:
        write = True
        break

    else:
        write = False

File.close()


def singleWrite():
    try:

        csvFile = open('Student Record.csv', 'a', newline='')
        csvWriter = csv.writer(csvFile)
        rollNum = int(input('Enter Roll Number:- '))
        name = input('Enter The Student Name:- ')
        marks = float(input('Enter Marks:- '))
        Entries = [rollNum, name, marks]
        csvWriter.writerow(Entries)

    except Exception as e:
        if str(e)[:39] == e1:
            print('Invalid Input Given In Roll Number!')
        if str(e)[:34] == e2:
            print('Invalid Input Given In Marks!')


def multiWrite():
    while True:
        try:
            csvFile = open('Student Record.csv', 'a', newline='')
            csvWriter = csv.writer(csvFile)
            rollNum = int(input('Enter Roll Number:- '))
            name = input('Enter The Student Name:- ')
            marks = float(input('Enter Marks:- '))
            Entries = [rollNum, name, marks]
            csvWriter.writerow(Entries)

            choice = input('Wish To Continue(Y/n):- ')
            if choice.lower() == 'n':
                break

        except Exception as e:
            if str(e)[:39] == e1:
                print('Invalid Input Given In Roll Number!')
            if str(e)[:34] == e2:
                print('Invalid Input Given In Marks!')


def showContent():
    csvFile = open('Student Record.csv', 'r')
    csvReader = csv.reader(csvFile)
    for rowI in csvReader:
        print(rowI)


print(
    '',
    'For Single Record Entry:- s',
    'For Multi Record Entries:- m',
    'For Seeing Content:- r',
    'To Exit:- x', sep='\n')

choiceI = input('Enter The Option:- ')
while True:
    if choiceI.lower() == 's':
        singleWrite()
        choiceI = input('Wish To Exit(X/n):- ')
    elif choiceI.lower() == 'm':
        multiWrite()
        choiceI = input('Wish To Exit(X/n):- ')
    elif choiceI.lower() == 'r':
        showContent()
        choiceI = input('Wish To Exit(X/n):- ')
    elif choiceI.lower() == 'x':
        break

    if choiceI.lower() != 'x':
        print(
            '',
            'For Single Record Entry:- s',
            'For Multi Record Entries:- m',
            'For Seeing Content:- r',
            'To Exit:- x', sep='\n')
        choiceI = input('Enter The Option:- ')
