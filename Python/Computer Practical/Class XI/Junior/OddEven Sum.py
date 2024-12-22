userRange = int(input("Enter A Range: "))

even = []
odd = []

for num in range(userRange):
    if num % 2 == 0:
        even.append(num)
    else:
        odd.append(num)

sumE = sum(even)
sumO = sum(odd)

print(f"Even Sum = {sumE}, Odd Sum = {sumO}")
