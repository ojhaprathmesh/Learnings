import string

String1 = string.ascii_letters
String2 = string.digits
String3 = string.punctuation
String = String1 + String2 + String3

List = list(String3)
del List[1]
del List[1]
del List[1]
del List[1]
del List[3]
del List[3]
del List[3]
del List[3]
del List[6]
del List[6]
del List[6]
del List[6]
del List[6]
del List[6]
del List[6]
del List[7]
del List[7]
del List[7]
del List[7]
del List[8]
del List[8]
del List[8]
del List[8]

strLen = len(String)

print(''.join(List))