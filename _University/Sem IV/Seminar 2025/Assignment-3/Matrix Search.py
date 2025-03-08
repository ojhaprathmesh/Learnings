def toArray():
    return list(map(int, input().split()))

m, n = toArray()
array = [toArray() for _ in range(m)]
target = int(input())

print(1 if any(target in row for row in array) else 0)
