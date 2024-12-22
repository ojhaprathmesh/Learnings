uName = input("Enter The Name :- ")
Physics = float(input('Physics Marks :- '))
Chemistry = float(input('Chemistry Marks :- '))
Maths = float(input('Maths Marks :- '))
CS = float(input('CS Marks :- '))
English = float(input('English Marks :- '))

#  ======== Main Calculation ========
Total = Physics + Chemistry + Maths + CS + English
Percentage = round(Total / 5, 2)
CGPA = round(Percentage / 10, 4)

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
print(f"\n"
         f"Student Name   : {uName}\n"
         f"Total Marks       : {Total}\n"
         f"Percentage        : {Percentage}%\n"
         f"CGPA                  : {CGPA}\n"
         f"Grade                 : {Grade}\n"
      )
