import numpy as np
import matplotlib.pyplot as plt


# ==== Functions ====

def rmvWhiteChar(Equation):
    reqList = list(Equation)
    reqLen = len(reqList)
    for i in range(len(reqList)):
        if reqList[i] == ' ':
            reqList[i] = 0
            reqLen -= 1
    while 0 in reqList:
        reqList.remove(0)
    reqStr = ''.join(reqList[0:reqLen])
    return reqStr


def compSeparation(symbolList, equation):  # ==== Component Separation ====
    tempDict = {}
    split = False
    for item in symbolList:
        if item in ('+', '-') and not split:
            split = True
            tempDict['x'] = equation.split(item)[0]
            tempDict['y'] = equation.split(item)[1].split('=')[0]
        if item == '=':
            tempDict['c'] = equation.split(item)[1]
    return tempDict


def coefExtraction(dictionary):
    for key in dictionary.keys():
        value = dictionary[key].split(key)[0]
        dictionary[key] = value
    return dictionary


def coefCorrection(var, dictionary):
    return dictionary[var] + '/' + dictionary['c']


# ==== Input And Variables ====

inpEquation = input('Enter The Equation:- ')
symbols = ('+', '-', '/', '*', '**', '^', '=')  # Symbols Used In An Equation
cordList = []  # Coordinate List

workEquation = rmvWhiteChar(inpEquation)
workDictionary = compSeparation(symbols, workEquation)
improvedDict = coefExtraction(workDictionary)
xCoef = eval(coefCorrection('x', improvedDict))
yCoef = eval(coefCorrection('y', improvedDict))

cordX = np.arange(-10, 10, 1)
cordY = (1 - xCoef * cordX) / yCoef  # y = (1-ax)/b

plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xlim(cordX[0], cordX[-1])
plt.ylim(cordY[0], cordY[-1])
plt.plot(cordX, cordY)
plt.title(workEquation)
plt.text(0, 0, '(0, 0)')
plt.show()
