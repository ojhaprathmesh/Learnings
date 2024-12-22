wish = True
while wish:
    #==========Main Processing==========#
    year = int(input('Enter The Year :- '))
    if year % 4==0 and year % 100!=0:
        print(f'{year} is a Leap Year')

    elif year % 4==0 and year % 100==0:
        if year % 400==0:
            print(f'{year} is a Leap Year')
        else:
            print(f'{year} is not a Leap Year')

    else:
        print(f'{year} is not a Leap Year')

    # ===========Asking Choice===========#
    choice = input('Do You Want To Continue(y/n) :- ')

    if choice=='y' or choice=='Y':
        wish = True
    elif choice=='n' or choice=='N':
        wish = False

    while choice!='y' and choice!='Y' and choice!='n' and choice!='N':
        print('Please Enter Correct Character')
        choice = input('Do You Want To Continue(y/n) :- ')

        if choice=='y' or choice=='Y':
            wish = True
        elif choice=='n' or choice=='N':
            wish = False