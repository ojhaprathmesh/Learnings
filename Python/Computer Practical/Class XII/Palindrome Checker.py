uInput = input('Enter The String :- ')
checkString = uInput[-1:]

for n in range(len(uInput)):
    checkString += uInput[(-n)-1:-n]

if uInput == checkString:
    print(f'\033[1;32;1m{uInput}\033[0m Is A Palindrome.')
else:
    print(f'\033[1;31;1m{uInput}\033[0m Is Not A Palindrome.')
