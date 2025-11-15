a = int(input("Enter A Number: "))
b = int(input("Enter A Number: "))
factList = []

for i in range(1, max(a, b)):
    if a % i == 0 and b % i == 0:
        factList.append(i)

print(f"HCF: {max(factList)}")
