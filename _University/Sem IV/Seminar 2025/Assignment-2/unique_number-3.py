def find_unique(int_array: list) -> int:
    ones, twos = 0, 0

    for num in int_array:
        ones = (ones ^ num) & ~twos  # bits that appear once
        twos = (twos ^ num) & ~ones  # bits that appear twice

    return ones  # The unique number is in `ones`


n = int(input())  # Number of elements
nums = list(map(int, input().split()))  # List of numbers

print(find_unique(nums))
