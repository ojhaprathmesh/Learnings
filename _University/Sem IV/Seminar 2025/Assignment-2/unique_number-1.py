n = int(input())  # Number of elements
nums = list(map(int, input().split()))  # List of n space-separated numbers

result = 0

for num in nums:
    result ^= num

print(result)
