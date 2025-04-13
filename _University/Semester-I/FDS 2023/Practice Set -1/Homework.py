from statistics import mean, median, mode

def myMean(*n):
    sum = 0
    for i in n:
        sum += i
    return sum/len(n)

"""
def myMedian(*n):
    medList = 0
    for i in n:
        medList.append(i)
    medList.sort()
    if medList%2==0:
    return 
"""

print(min(1,2,4,45,2,4,2,4,2,4,5))
print(max(1,2,4,45,2,4,2,4,2,4,5))
print(mean([1,2,3,4,5,6,7,8,9]))
print(median([1,2,3,4,5,7,9,5,6,7,8,9]))
print(mode([1,2,3,4,5,6,7,8,9]))
print(abs(-54))