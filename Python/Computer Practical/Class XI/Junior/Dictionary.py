oxford = {'Iatrochemistry': "study of chemistry in relation to"
          "the physiology, pathology, and treatment of disease",
          'Sabotage': "any underhand interference"
          "with production or work by enemy",
          'Habilitate': "to become fit",
          'Ichthyolite': "a fossil fish",
          'Tactician': "a person who is adept in planning tactics",
          'Apologise': "express regret for something that one has done wrong",
          }

run = True
print("\n1: Show Dictionary Items"
          "\n2: Show Word Meaning"
          "\n3: Add Words To Dictionary"
          "\n4: Update Meaning\n")
while run:
    choice = input("Enter The Choice: ")
    while not choice.isdigit():
        choice = input("Enter The Choice Correctly: ")
    choice = int(choice)

    if choice == 1:
        dispValue = enumerate(oxford)
        for i in dispValue:
            print(f"{i[0]+1} : {i[1]}")

    if choice == 2:
        word = input("Enter The Word: ")
        if word in oxford.keys():
            print(f"\n{word}: {oxford[word]}")
        else:
            print("Word Not Found!")

    if choice == 3:
        word = input("Enter The Word: ")
        meaning = input("Enter Meaning Of Word: ")
        oxford[word] = meaning

    if choice == 4:
        word = input("Enter The Word To Be Updated: ")
        if word in oxford.keys():
            oxford[word] = input("Enter The New Meaning: ")
        else:
            print("Word Not Found!!")

    print("\nY: To Exit"
          "\nAnything Else To Continue")
    exChoice = input("Want To Exit(Y/n): ")
    if exChoice.lower() == 'y':
        run = False
