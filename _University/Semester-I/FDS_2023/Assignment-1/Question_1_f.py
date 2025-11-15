fibonnaci = []
n = int(input("Enter Number Of Elements: "))
for i in range(n):
    if len(fibonnaci) < 2:
        fibonnaci.append(i)
    else:
        fibonnaci.append(fibonnaci[i-2] + fibonnaci[i-1])

for i in fibonnaci:
    print(i, end=' ')
