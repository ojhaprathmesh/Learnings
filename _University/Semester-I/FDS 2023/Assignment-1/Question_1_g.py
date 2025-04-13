num = 1
n = int(input("Enter a number: "))
tempList = []
while num <= n:
    output = True
    for i in range(2, num):
        if num % i == 0 and 1 not in [i, num]:
            output = False
    if output and num != 1:
        tempList.append(num)
    num += 1

if n in tempList:
    print("Prime Number")
else:
    print("Not A Prime Number")
