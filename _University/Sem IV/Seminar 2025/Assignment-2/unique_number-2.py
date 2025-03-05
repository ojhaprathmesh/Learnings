def find_two_unique_numbers(int_array: list) -> (int, int):
    xor_all = 0
    for num in int_array:
        xor_all ^= num  # This cancels out the pairs, leaving a ^ b

    set_bit = xor_all & -xor_all  # This gives the rightmost set bit

    num1, num2 = 0, 0
    for num in int_array:
        if num & set_bit:  # Group 1: numbers with the set bit
            num1 ^= num
        else:  # Group 2: numbers without the set bit
            num2 ^= num

    return num1, num2


n = int(input())  # Number of elements
nums = list(map(int, input().split()))  # List of numbers

num1, num2 = find_two_unique_numbers(nums)
print(min(num1, num2), max(num1, num2))
