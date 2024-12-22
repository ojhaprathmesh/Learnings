# def abc(a, b, c):
#     return a*2, b*2, c*2
# print(abc(1, 2, 3))
#
# def display(s):
#     length = len(s)
#     m = ""
#     for i in range(0, length):
#         if s[i].isupper():
#             m += s[i].lower()
#         elif s[i].islower():
#             m += s[i].upper()
#         elif s[i].isdigit():
#             m += '$'
#         else:
#             m += '*'
#     print(m)
#
#
# display("EXAM20@cbse.com")
# import antigravity
#
# def Total(Number=10):
#     Sum = 0
#     for C in range(1, Number+1):
#         if C % 2 == 0:
#             continue
#         Sum += C
#     return Sum
#
# print(Total(4))
# print(Total(7))
# print(Total())
#
# X = 50
# def Change(P=10, Q=25):
#     global X
#     if P % 6 == 0:
#         X += 100
#     else:
#         X += 50
#     Sum = P + Q + X
#     print(P, '#', Q, '$', Sum)
#
# Change()
#
# Change(18, 50)
#
# Change(30, 100)
#
# def JumbleUp(mystr):
#     L = len(mystr)
#     str2 = ''
#     str3 = ''
#     for i in range(0, L, 2):
#         str2 = str2 + mystr[i+1] + mystr[i]
#         for ch in str2:
#             if ch >= 'R' and ch <= 'U':
#                 str3 += '$'
#             else:
#                 str3 += ch.lower()
#     return str3
#
# mystr = "HARMONIOUS"
# mystr = JumbleUp(mystr)
# print(mystr)
# def display(x=2, y=3):
#     x += y
#     y += 2
#     print(x,y)
#
# display()
# display(5,1)
# display(9)
#
# def b():
#     print('Hello')
#
#     def a():
#         print('How Are You')
#
#     a()
#     b()
# b()
#
# from Modules import TestModule as Tm
#
# print(Tm.add(1, 9, 10))
#
# from Modules import Physics
#
# print(Physics.speed())
# print(Physics.speed(100, 20))
# print(Physics.velocity1d())
# print(Physics.velocity1d(20, 5))
# print(Physics.velocity2d())
# print(Physics.velocity2d((0, 1), (4, 4), 2))
# print(Physics.displacement1d())
# print(Physics.displacement1d(20, 15))
# print(Physics.displacement2d())
# print(Physics.displacement2d((6, 9), (2, 6)))
#
# import time
# import sys
# #first text
# print('Hey.', end="")
# #flush stdout
# sys.stdout.flush()
# #wait a second
# time.sleep(1)
# #write a carriage return and new text
# print('\rHow is your day?')

