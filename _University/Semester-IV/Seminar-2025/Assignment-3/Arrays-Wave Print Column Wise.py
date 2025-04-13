def toArray():
    return list(map(int, input().split()))

m, n = toArray()
array = [toArray() for _ in range(m)]

for col in range(n):
    if col % 2 == 0:
        for row in range(m):
            print(array[row][col], end=", ")
    else:
        for row in range(m - 1, -1, -1):  # Reverse order for odd columns
            print(array[row][col], end=", ")

print("END")
