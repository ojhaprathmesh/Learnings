def print_pattern(num):
    a = '*'
    for i in range(0, num):
        print(a)
        a += '*'


Num = int(input('Enter Pattern Length In Numbers :- '))

print_pattern(Num)
