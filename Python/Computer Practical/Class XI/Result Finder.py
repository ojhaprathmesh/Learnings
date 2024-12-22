student = int(input('Enter The Number Of Students :- '))
Grade = None
Result = None

for i in range(0, student):  # Data Input
    uName = input("Enter The Name :- ")
    Physics = int(input('Physics Marks :- '))
    Chemistry = int(input('Chemistry Marks :- '))
    Maths = int(input('Maths Marks :- '))
    CS = int(input('CS Marks :- '))
    English = int(input('English Marks :- '))

    #  ======== Main Calculation ========
    Total = Physics + Chemistry + Maths + CS + English
    Percentage = round(Total / 5, 2)
    CGPA = round(Percentage / 10, 4)

    #  ======== Functions ========
    def checkPass():
        if Physics <= 32:
            Pass = 'Fail'

        elif Chemistry <= 32:
            Pass = 'Fail'

        elif Maths <= 32:
            Pass = 'Fail'

        elif CS <= 32:
            Pass = 'Fail'

        elif English <= 32:
            Pass = 'Fail'

        else:
            Pass = 'Pass'

        return Pass


    def comments(cgpa):
        if cgpa == 10:
            comment = 'Fabulous Performance'

        elif 9 < cgpa < 10:
            comment = 'Excellent Performance\nKeep It Up'

        elif 7 < cgpa < 9:
            comment = 'Good Performance'

        elif 3.2 < cgpa < 7:
            comment = 'Average Performance\nWork Harder!'

        else:
            comment = 'Lots Of Hard Work Required!!'

        return comment


    if Percentage > 90:
        Grade = 'A1'

    elif 80 < Percentage <= 90:
        Grade = 'A2'

    elif 70 < Percentage <= 80:
        Grade = 'B1'

    elif 60 < Percentage <= 70:
        Grade = 'B2'

    elif 50 < Percentage <= 60:
        Grade = 'C1'

    elif 40 < Percentage <= 50:
        Grade = 'C2'

    elif 30 < Percentage <= 40:
        Grade = 'D1'

    elif 20 < Percentage <= 30:
        Grade = 'D2'

    elif 10 < Percentage <= 20:
        Grade = 'E1'

    elif Percentage <= 10:
        Grade = 'E2'

    print(f"\nStudent Name :- {uName}\n"
          f'Total Marks :- {Total}\n'
          f'Average Marks :- {Percentage}%\n'
          f'CGPA :- {CGPA}\n'
          f'Grade :- {Grade}\n'
          f'{checkPass()}ed\n'
          f'{comments(CGPA)}\n')
