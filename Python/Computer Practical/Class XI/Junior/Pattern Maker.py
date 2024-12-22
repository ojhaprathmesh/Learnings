# nList = []
#
# for i in range(2, 7):
#     for j in range(1, len(nList) + i):
#         if j in nList:
#             continue
#         print('#', end=' ')
#         if j not in nList:
#             nList.append(j)
#     print()

aList = ['A', 'B', 'C', 'D', 'E']
n = len(aList)
for i in range(n):
    for j in range(n):
        if j > i:
            continue
        print(aList[j], end=' ')
    print()