inpList1 = list(input("Enter 1st String:- ").lower()).sort()
inpList2 = list(input("Enter 2nd String:- ").lower()).sort()

if inpList1 == inpList2:
    print("Anagram Detected")

else:
    print("Not An Anagram")
