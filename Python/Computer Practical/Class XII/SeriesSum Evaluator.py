from math import factorial

x = 0
fact = 1
result = 1

try:
    repeat = int(input('Enter The No. Of Repetition :- '))
    x += 1
    varX = int(input('Enter The Value Of X :- '))

    for i in range(1, repeat+1):
        result += (varX/factorial(i-1))
    result = round(result, 8)

    print(result)

except Exception as e:
    if x == 0:
        print('Please Enter The Repetition In Integer Form Only')
    elif x == 1:
        print('Please Enter The Value Of X In Integer Form Only')

    print(e)
