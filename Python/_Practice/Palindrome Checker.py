def checkStr(str):
    if str[::-1].lower() == str.lower():
        return True
    else:
        return False


print(checkStr(input("Enter A String To Check For Palindrome:- ")))
