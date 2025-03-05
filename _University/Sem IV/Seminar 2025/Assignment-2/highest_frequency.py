n = int(input())
nums = list(map(int, input().split()))

table = {}
max_freq = float('-inf')
max_freq_num = None

# Count frequency of each number
for num in nums:
    table[num] = table.get(num, 0) + 1

# Find the number with the maximum frequency
for key, value in table.items():
    if value > max_freq:
        max_freq = value
        max_freq_num = key

print(max_freq_num)
