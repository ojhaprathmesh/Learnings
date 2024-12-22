# stdList = [['Kali', '11', 439]]
# run = True
#
# print("1: Add Student Details\n"
#            "2: Show Student Details\n"
#            "3: Modify Details\n"
#            "4: Delete Detail From Given Position\n"
#            "5: Delete Detail With Given Info")
#
# while run:
#     choice = int(input(f"Enter The Choice: "))
#
#     if choice == 1:
#         name = input("Enter Student Name: ")
#         grade = input("Enter Student Class: ")
#         marks = eval(input("Enter Student Marks: "))
#         stdList.append([name, grade, marks])
#
#     if choice == 2:
#         if len(stdList) > 0:
#             print(f"\n{stdList}\n")
#         else:
#             print('No Information Available!')
#
#     if choice == 3:
#         print("1: Change Name\n"
#               "2: Change Class\n"
#               "3: Change Marks")
#         posCh = int(input(f"Position Of Details:"))
#         inpCh = int(input(f"Enter The Choice: "))
#         stdList[posCh][inpCh - 1] = input("Enter The New Detail: ")
#
#     if choice == 4:
#         posChoice = int(input(f"Position Of Details:"))
#         if len(stdList) == 0:
#             print("No Details To Delete!!")
#             break
#         else:
#             del stdList[posChoice]
#
#     if choice == 5:
#         if len(stdList) == 0:
#             print("No Details To Delete!!")
#             break
#         posChoice = int(input(f"Position Of Student Detail:"))
#         delValue = input("Detail To Be Searched: ")
#         for value in stdList[posChoice]:
#             if value == delValue:
#                 del stdList[posChoice]
#
#     print("Y: To Exit\n"
#           "Anything Else To Continue")
#     exChoice = input("Want To Exit(Y/n): ")
#     if exChoice.lower() == 'y':
#         run = False

record = {}
while True:
    name = input("Enter Student Name: ")
    mCount = int(input(f"Enter {name}'s Medal Count: "))

    record[name] = mCount

    if input("Want To Exit(Y/n): ").lower() == 'y':
        break

print(record)