size = int(input())
k = int(input())
array = sorted(list(map(int, input().split())))

print(array[size - k])
