print("1 for Add\n"
      "2 for Sub\n"
      "3 for Multiply\n"
      "4 for Division")

num1 = int(input("Enter A Number:- "))
num2 = int(input("Enter A Number:- "))

choice = input("Enter A Choice:- ")
# while not choice.isdigit():
#     choice = input("Enter A Correct Choice:- ")
# choice = int(choice)

if choice == '+':
    print(num1+num2)

elif choice == '-':
    print(num1-num2)

elif choice == '*':
    print(num1*num2)

elif choice == '/':
    if num2 != 0:
        print(num1/num2)

    else:
        print("Zero Division Not Allowed")

else:
    print("Invalid Choice")