first = int(input('First Number(A) :- '))
second = int(input('Second Number(B) :- '))
third = int(input('Third Number(C) :- '))

while first == second or first == third or second == third:
    if first == second:
        print('A = B')

    elif first == third:
        print('A = C')

    else:
        print('B = C')

    print('Please Give Different Numbers')
    third = int(input('Third Number(C) :- '))

if first < second:
    if second < third:
        print('A < B < C')
        print('C is Largest Number')

    elif second > third:
        if first < third:
            print('A < C < B')
            print('B is Largest Number')

        elif first > third:
            print('C < A < B')
            print('B is Largest Number')

elif first > second:
    if second > third:
        print('C < B < A')
        print('A is Largest Number')

    elif second < third:
        if first < third:
            print('B < A < C')
            print('C is Largest Number')

        elif first > third:
            print('B < C < A')
            print('A is Largest Number')