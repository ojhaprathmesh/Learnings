from math import pi

print("1 for Squaring\n"
      "2 for Cubing\n"
      "3 for Circle Area")

num = int(input("Enter A Number:- "))

choice = input("Enter A Choice:- ")
while not choice.isdigit():
    choice = input("Enter A Correct Choice:- ")
choice = int(choice)

if choice == 1:
    print(num ** 2)

elif choice == 2:
    print(num ** 3)

elif choice == 3:
    print(round(pi * num ** 2, 2))

else:
    print("Invalid Choice")
