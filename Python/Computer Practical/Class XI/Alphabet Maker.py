size = int(input('Enter The Size :- '))


# for i in range(0,size):
#     for j in range(0,size):
#         print('*', end=' ')
#     print('\n',end='')

def writeA(length):
    edge = length // 3
    factor = edge // 3 + 1

    for i in range(0, length):
        for j in range(0, length):
            if edge <= j <= edge + factor: # and edge + factor > i > edge - factor - 1:
                print(' ', end=' ')
                continue
            if j == length - 1:
                print('*', end='')
            else:
                print('*', end=' ')

        print('\n', end='')


writeA(size)
