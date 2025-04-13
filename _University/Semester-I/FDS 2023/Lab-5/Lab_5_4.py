fib = []  # List to contain the sequence numbers
n = int(input("Enter A Number: "))
for i in range(n):
    if len(fib) < 2:
        fib.append(i)  # This initiates the sequence
    else:
        fib.append(fib[i - 2] + fib[i - 1])  # This extends the sequence

print(fib)
