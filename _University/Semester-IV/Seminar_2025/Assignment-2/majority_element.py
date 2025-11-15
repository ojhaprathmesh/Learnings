def find(factor: float, int_array: list) -> int:
    table = {}
    for num in int_array:
        table[num] = table.get(num, 0) + 1

    for num in table.keys():
        if table[num] > factor:
            return num

    return -1


size = int(input())
nums = list(map(int, input().split()))
result = find(size / 2, nums)
print(result)
