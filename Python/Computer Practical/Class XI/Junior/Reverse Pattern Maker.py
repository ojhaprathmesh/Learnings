for i in range(5, 0, -1):
    print('  ' * abs(i - 5), end='')
    for j in range(i, 0, -1):
        print("@", end='')
    print('\n', end='')
