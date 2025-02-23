def isPalindrome(num : str) -> bool:
    return num == num[::-1]

print(isPalindrome(input()))