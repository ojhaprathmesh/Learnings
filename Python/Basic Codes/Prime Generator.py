import time

Number = 1
Index = 0
Wish = True


def primeCheckEven():
    for num in Prime:
        if num / 2 != 1 and num % 2 == 0:
            Index1 = Prime.index(num)
            del Prime[Index1]


def primeCheckOdd():
    for num in Prime:
        for Index2 in range(0, len(Prime)):
            if Index2 < len(Prime):
                if Prime[Index2] / num != 1 and Prime[Index2] % num == 0:
                    del Prime[Index2]


def confirmPrime():
    for num in Prime:
        for Index3 in range(0, len(Prime)):
            if Index3 < len(Prime):
                if Prime[Index3] / num != 1 and Prime[Index3] % num == 0:
                    del Prime[Index3]


Prime = []

# while Wish:
limitUpper = int(input('Enter The Max Limit :- '))
initialTime = time.time()

while Number != limitUpper:
    for i in range(2, Number + 2):
        if i not in Prime:
            Prime.append(i)
    Number += 1

primeCheckEven()
primeCheckOdd()
# confirmPrime()

finalTime = time.time()

Time = round(finalTime - initialTime, 5)

print(f'Primes :- {Prime}')
print(f'Time Taken :- {Time}')
#
# Choice = input('Do You Want To Continue(y/n) :- ')
# while Choice!='y' and Choice!='n':
#     print('Invalid Input!!')
#     print('Kindly Provide Input In LowerCase')
#     Choice = input('Do You Want To Continue(y/n) :- ')
#
# if Choice=='y':
#     Wish = True
# elif Choice=='n':
#     Wish = False
