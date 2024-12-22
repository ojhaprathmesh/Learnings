UInput = int(input('Enter The Number :- '))  # User Input
Numbers = []  # Empty List
x = 0

if (UInput % 2 == 0 and UInput != 2) or UInput == 1:
    print(f'\033[1;31;1m{UInput}\033[0;32;0m Is Not A Prime Number.')

else:
    for Num in range(2, UInput):
        if Num % 2 != 0 and Num != 2:
            Numbers.append(Num)

    for i in range(len(Numbers)):
        for j in range(len(Numbers)):
            if UInput == i*j and x < 1:
                print(f'\033[1;31;1m{UInput}\033[0m Is Not A Prime Number.')
                x += 1
            elif x < 1:
                print(f'\033[1;32;1m{UInput}\033[0m Is A Prime Number.')
                x += 1
