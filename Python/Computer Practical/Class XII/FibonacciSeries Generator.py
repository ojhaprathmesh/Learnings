def fibonacci(uInput):
    fList = [1]
    result = 1
    for i in range(uInput):
        result += i
        fList.append(result)

    return fList


n = int(input('Enter Max Distinct Elements :- '))
print(fibonacci(n))
