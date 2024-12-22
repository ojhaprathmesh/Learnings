print("Use Numerals Only To Use All Commands\n"
          "1: Index\n"
          "2: Sorting\n"
          "3: Count A Item\n"
          "4: Find Minimum\n"
          "5: Find Maximum")

inpTuple = eval(input('Enter The Tuple: '))
inpTuple = tuple(inpTuple)
print(inpTuple)

def give(disp):
    inp = input(f"Enter The {disp}: ")
    while not inp.isdigit():
        inp = input(f"Enter {disp} Correctly: ")

    return int(inp)

def askExit():
    print("Y: To Exit\n"
          "Anything Else To Continue")
    exChoice = input("Want To Exit(Y/n): ")
    if exChoice.lower() == 'y':
        return False
    return True

run = True
while run:
    choice = give('Choice')
    if choice == 1:
        value = eval(input("Enter The Element To Be Indexed: "))
        if value in inpTuple:
            print(f"The Position Of '{value}' Is {inpTuple.index(value)}")
        else:
            print(f"'{value}' Not Found !!")
        run = askExit()

    if choice == 2:
        allowed = True
        for i in inpTuple:
            if type(i) != int:
                allowed = False
        if allowed:
            print(inpTuple)
            inpTuple = tuple(sorted(inpTuple))
            print(inpTuple)
        else:
            print("Sorting is Not Possible!")
        run = askExit()

    if choice == 3:
        value = eval(input("Enter The Element To Be Counted: "))
        print(f"Element '{value}' Has Occurred {inpTuple.count(value)} Times")
        run = askExit()

    if choice == 4:
        print(f"Minimum In {inpTuple} is {min(inpTuple)}")
        run = askExit()

    if choice == 5:
        print(f"Maximum In {inpTuple} is {max(inpTuple)}")
        run = askExit()
