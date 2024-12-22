userStr = input("Enter A String: ")
vowelList = ['a', 'e', 'i', 'o', 'u']
strList = userStr.split(' ')

print("1: Words Starting With Vowels")
print("2: Words With 4+ Characters")
print("3: Print In Uppercase")

choice = int(input("Enter A Choice(1/2/3): "))
for item in strList:
    if item[0].lower() in vowelList and choice == 1:
        print(item)

    if len(item) > 4 and choice == 2:
        print(item)

    if choice == 3:
        print(userStr.upper())
        break
