a1 = int(input('Enter The First Term :- '))
a2 = int(input('Enter The Second Term :- '))
n = int(input('Enter The Number Of Progressions :- '))

d = a2-a1
for i in range(0,n):
    an = a1+(i)*d
    print(an)