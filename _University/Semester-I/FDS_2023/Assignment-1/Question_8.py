string = "hello world@ 123"
letCount = 0
numCount = 0

for char in string:
    if char.isdigit():
        numCount += 1
    if char.isalpha():
        letCount += 1

print(f"Letters: {letCount}")
print(f"Numbers: {numCount}")
