def toArray() -> list[int]:
	return list(map(int, input().split()))

m, n = toArray()
array = [[] for _ in range(m)]

for i in range(m):
	array[i] = toArray()

for row in range(m):
	for col in range(n):
		if row % 2 == 0:
			print(array[row][col], end=", ")
		else:
			print(array[row][n - col - 1], end=", ")

print("END")