import pickle
from random import *
import math

# tup1 = (10, 20, 30, 40, 50, 60, 70, 80, 90)
# print(tup1[3:7:2])
#
# lst1 = [1,2,3,4]
# with open('record.bin','wb') as myfile:
#     pickle.dump(lst1,myfile)
# T=(100)
# print(T*2)
# myfile = open("abc.txt")
# data = myfile.readlines()
# print(len(data))
# myfile.close()
# lst1 = [10, 15, 20, 25, 30]
# lst1.insert(3, 4)
# print(lst1)
# lst1.insert(2, 3)
# print(lst1)
# print (lst1[-5])
# x = ("ONe",)
# print(type(x))
# S='Welcome'
# def Change(T):
#     T = 'Hello'
#     print(T,end='@')
# Change(S)
# print(S)
# f = open('Rhymes.txt')
# s = f.read()
# l = s.split()
# for i in l:
#     if len(i) % 3 != 0:
#         print(i, end=" ")
V = 25
def Fun(ch):
    V = 50
    print(V, end=ch)
    V *= 2
    print(V, end=ch)
print(V, end='*')
Fun('!')
print(V)