def is_palindrome(num: str) -> bool:
    return num == num[::-1]


print(is_palindrome(input()))
