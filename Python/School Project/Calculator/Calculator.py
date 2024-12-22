import ctypes
from math import *
from tkinter import *
from os import system, getcwd, chdir

MyAppId = 'D://Python//Calculator//Icon.ico'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(MyAppId)


class myProject:
    def __init__(self):
        self.root = root
        self.root.geometry('425x544+450+100')
        self.root.title('Calculator | Developed by Prathmesh')
        self.root.resizable(False, False)
        self.root.iconbitmap('Icon.ico')

        # ======== Menu Related Widgets ========

        mainMenu = Menu(self.root)
        gameMenu = Menu(mainMenu, tearoff=0)
        aboutMenu = Menu(mainMenu, tearoff=0)

        def executeMemory():
            chdir(getcwd())
            system("python Memory.py")

        def executeTiles():
            chdir(getcwd())
            system("python Tiles.py")

        def dummy():
            pass

        gameMenu.add_command(label='Memory', command=executeMemory)
        gameMenu.add_command(label='Tiles', command=executeTiles)
        aboutMenu.add_command(label='Under Coding', command=dummy)

        mainMenu.add_cascade(label='Games', menu=gameMenu)
        mainMenu.add_cascade(label='About', menu=aboutMenu)

        self.root.config(menu=mainMenu)

        # ======== Variables ========
        self.txtEntry1 = StringVar()
        self.txtEntry2 = StringVar()
        self.inpValue = StringVar()
        self.modIndicationNum = 0
        self.signList = ['×', '\u00F7', '+', '\u2212']
        self.baseOperationSymbols = ['*', '/', '+', '-']
        self.trigRatios = ['sin(', 'cos(', 'tan(', 'cot(', 'sec(', 'cosec(']
        self.digits = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
        self.endBracket = 0
        self.trigEval = 0
        self.allowNum = 1
        self.tmpList = []

        # ======== Coloring Title ========
        colTitle = Label(self.root, bg='black')
        colTitle.place(x=0, y=0, width=425, height=524)

        # ========  Output Frame  ========

        txtFrame = Frame(self.root, bd=4, relief=RIDGE, bg='white')
        txtFrame.place(x=5, y=5, width=415, height=110)

        showTxt = Entry(txtFrame, font=('times new roman', 16, 'bold'), justify=RIGHT, state='disabled',
                        textvariable=self.txtEntry2, bd=1, bg='white')
        showTxt.place(x=0, y=0, relwidth=1, relheight=0.4)

        inpText = Entry(txtFrame, font=('times new roman', 32, 'bold'), justify=RIGHT, textvariable=self.txtEntry1,
                        bd=1, bg='light grey')
        inpText.place(x=0, rely=0.4, relwidth=1, relheight=0.6)

        # ======== Input Frame ========

        cmdFrame = Frame(self.root, bd=4, relief=RIDGE, bg='grey')
        cmdFrame.place(x=5, y=120, width=415, height=398)

        def secondFunc():
            if self.modIndicationNum % 2 != 0:
                secButtons1()

            else:
                secButtons2()

            self.modIndicationNum += 1

        def secButtons1():
            btn_2 = Button(cmdFrame, text='x\u00B2', command=self.sqrX, font=('times new roman', 20, 'bold'),
                           bg='#2100ff', fg='white')
            btn_2.place(x=5, y=60, width=75, height=50)

            btn_3 = Button(cmdFrame, text='\u221Ax', command=self.sqrRT, font=('times new roman', 20, 'bold'),
                           bg='#2100ff', fg='white')
            btn_3.place(x=5, y=115, width=75, height=50)

            btn_4 = Button(cmdFrame, text='x\u02B8', command=self.xExp, font=('times new roman', 20, 'bold'),
                           bg='#2100ff', fg='white')
            btn_4.place(x=5, y=170, width=75, height=50)

            btn_5 = Button(cmdFrame, text='10\u036F', command=self.tenExp, font=('times new roman', 20, 'bold'),
                           bg='#2100ff', fg='white')
            btn_5.place(x=5, y=225, width=75, height=50)

            btn_6 = Button(cmdFrame, text='log', command=self.logX, font=('times new roman', 20, 'bold'),
                           bg='#2100ff', fg='white')
            btn_6.place(x=5, y=280, width=75, height=50)

            btn_7 = Button(cmdFrame, text='ln', command=self.lnX, font=('times new roman', 20, 'bold'),
                           bg='#2100ff', fg='white')
            btn_7.place(x=5, y=335, width=75, height=50)

        def secButtons2():
            btn_2 = Button(cmdFrame, text='sin', command=self.sin, font=('times new roman', 20, 'bold'),
                           bg='#2100ff', fg='black')
            btn_2.place(x=5, y=60, width=75, height=50)

            btn_3 = Button(cmdFrame, text='cos', command=self.cos, font=('times new roman', 20, 'bold'),
                           bg='#2100ff', fg='black')
            btn_3.place(x=5, y=115, width=75, height=50)

            btn_4 = Button(cmdFrame, text='tan', command=self.tan, font=('times new roman', 20, 'bold'),
                           bg='#2100ff', fg='black')
            btn_4.place(x=5, y=170, width=75, height=50)

            btn_5 = Button(cmdFrame, text='cot', command=self.cot, font=('times new roman', 20, 'bold'),
                           bg='#2100ff', fg='black')
            btn_5.place(x=5, y=225, width=75, height=50)

            btn_6 = Button(cmdFrame, text='sec', command=self.sec, font=('times new roman', 20, 'bold'),
                           bg='#2100ff', fg='black')
            btn_6.place(x=5, y=280, width=75, height=50)

            btn_7 = Button(cmdFrame, text='cosec', command=self.cosec, font=('times new roman', 20, 'bold'),
                           bg='#2100ff', fg='black')
            btn_7.place(x=5, y=335, width=75, height=50)

        btn_1 = Button(cmdFrame, text='2\u207F\u1D48', command=secondFunc, font=('times new roman', 20),
                       bg='#2100ff', fg='white')
        btn_1.place(x=5, y=5, width=75, height=50)

        secButtons1()  # To Save Some Lines, Compiled A Group Of Buttons (2-7) Into Function.

        btn_8 = Button(cmdFrame, text='\u03C0', command=self.constantPi, font=('times new roman', 20),
                       bg='#2100ff', fg='white')
        btn_8.place(x=85, y=5, width=75, height=50)

        btn_9 = Button(cmdFrame, text='1/x', command=self.numX, font=('times new roman', 20, 'bold'),
                       bg='#2100ff', fg='white')
        btn_9.place(x=85, y=60, width=75, height=50)

        btn_10 = Button(cmdFrame, text='(', command=self.openBracket1, font=('times new roman', 20),
                        bg='#2100ff', fg='white')
        btn_10.place(x=85, y=115, width=75, height=50)

        btn_14 = Button(cmdFrame, text='\u00B1', command=self.negate, font=('times new roman', 24, 'bold'),
                        bg='#2100ff', fg='white')
        btn_14.place(x=85, y=335, width=75, height=50)

        btn_15 = Button(cmdFrame, text='e', command=self.eConstant, font=('times new roman', 20),
                        bg='#2100ff', fg='white')
        btn_15.place(x=165, y=5, width=75, height=50)

        btn_16 = Button(cmdFrame, text='|x|', command=self.modX, font=('times new roman', 20, 'bold'),
                        bg='#2100ff', fg='white')
        btn_16.place(x=165, y=60, width=75, height=50)

        btn_17 = Button(cmdFrame, text=')', command=self.openBracket2, font=('times new roman', 20),
                        bg='#2100ff', fg='white')
        btn_17.place(x=165, y=115, width=75, height=50)

        btn_21 = Button(cmdFrame, text='0', command=self.num0, font=('times new roman', 25),
                        bg='#2100ff', fg='white')
        btn_21.place(x=165, y=335, width=75, height=50)

        btn_22 = Button(cmdFrame, text='C', command=self.clear, font=('times new roman', 20),
                        bg='#2100ff', fg='white')
        btn_22.place(x=245, y=5, width=75, height=50)

        btn_23 = Button(cmdFrame, text='exp', command=self.tenMultiplier, font=('times new roman', 20),
                        bg='#2100ff', fg='white')
        btn_23.place(x=245, y=60, width=75, height=50)

        btn_24 = Button(cmdFrame, text='n!', command=self.factorialNum, font=('times new roman', 20),
                        bg='#2100ff', fg='white')
        btn_24.place(x=245, y=115, width=75, height=50)

        btn_28 = Button(cmdFrame, text='.', command=self.decimal, font=('times new roman', 25),
                        bg='#2100ff', fg='white')
        btn_28.place(x=245, y=335, width=75, height=50)

        btn_29 = Button(cmdFrame, text='Del', command=self.delLast, font=('times new roman', 20,),
                        bg='#2100ff', fg='white')
        btn_29.place(x=325, y=5, width=75, height=50)

        btn_30 = Button(cmdFrame, text='mod', command=self.modulus, font=('times new roman', 20),
                        bg='#2100ff', fg='white')
        btn_30.place(x=325, y=60, width=75, height=50)

        btn_35 = Button(cmdFrame, text='=', command=self.equalsTo, font=('times new roman', 24, 'bold'),
                        bg='#2100ff', fg='white')
        btn_35.place(x=325, y=335, width=75, height=50)

        for sign in self.signList:
            num = self.signList.index(sign)
            yInc = num * 55  # Increment In y-axis
            button = Button(cmdFrame, text=sign, command=lambda x=sign: self.baseOperations(x),
                            font=('times new roman', 32), bg='#2100ff', fg='white')
            button.place(x=325, y=115 + yInc, width=75, height=50)

        for text, num in self.digits.items():
            if num % 3 == 0:
                yInc = (num // 3 - 1) * 55  # Increment In y-axis
                button = Button(cmdFrame, text=text, command=lambda x=num: self.valButton(x),
                                font=('times new roman', 25),
                                bg='#2100ff', fg='white')
                button.place(x=245, y=170 + yInc, width=75, height=50)

            if num % 3 == 1:
                yInc = (num // 3) * 55  # Increment In y-axis
                button = Button(cmdFrame, text=text, command=lambda x=num: self.valButton(x),
                                font=('times new roman', 25),
                                bg='#2100ff', fg='white')
                button.place(x=85, y=170 + yInc, width=75, height=50)

            if num % 3 == 2:
                yInc = (num // 3) * 55  # Increment In y-axis
                button = Button(cmdFrame, text=text, command=lambda x=num: self.valButton(x),
                                font=('times new roman', 25),
                                bg='#2100ff', fg='white')
                button.place(x=165, y=170 + yInc, width=75, height=50)

        if self.getTxt1() == '':  # Limiting The Value From Displaying Nothing
            self.setTxt1('0')

        def bindKeys():
            bindObj = self.root
            bindObj.bind("prathmesh", lambda event, name='prathmesh': self.hello(name))
            bindObj.bind("exclam", lambda event: self.factorialNum())
            bindObj.bind("<Escape>", lambda event: self.clear())
            bindObj.bind("<Shift_L>", lambda event: secondFunc())
            bindObj.bind("<Return>", lambda event: self.equalsTo())
            bindObj.bind("<BackSpace>", lambda event: self.delLast())
            bindObj.bind("<parenleft>", lambda event: self.openBracket1())
            bindObj.bind("<parenright>", lambda event: self.openBracket2())

            for key in self.digits:
                bindObj.bind(str(key), lambda event, digit=key: self.valButton(digit))

            for symbol in self.baseOperationSymbols:
                bindObj.bind(symbol, lambda event, operator=symbol: self.baseOperations(operator))

        bindKeys()

    # ======== Commonly Used Commands ========
    def setTxt1(self, txt):
        return self.txtEntry1.set(txt)

    def getTxt1(self):
        return self.txtEntry1.get()

    def setTxt2(self, txt):
        return self.txtEntry2.set(txt)

    def getTxt2(self):
        return self.txtEntry2.get()

    def hello(self, name):
        if name == 'prathmesh':
            self.setTxt1('A Hello By Prathmesh')

    # ======== Numeral Input Commands ========

    def valButton(self, num):
        if self.allowNum == 1:
            if self.getTxt1() == '0':
                self.setTxt1(str(num))
            elif self.getTxt2()[-1:] == '=':
                self.setTxt1(str(num))
            else:
                self.setTxt1(self.getTxt1() + str(num))

            if self.getTxt2() == '':
                self.setTxt2(str(num))
            elif self.getTxt2() == '0':
                self.setTxt2(str(num))
            elif self.getTxt2()[-1:] == '=':
                self.setTxt2(str(num))
            else:
                self.setTxt2(self.getTxt2() + str(num))

    def num0(self):
        if self.allowNum == 1:
            if self.getTxt2()[-1:] == '=':
                self.setTxt1('0')
            elif self.getTxt1() != '0':
                self.setTxt1(self.getTxt1() + '0')

            if self.getTxt2()[-1:] == '=':
                self.setTxt1('0')
            elif self.getTxt2() != '':
                self.setTxt2(self.getTxt2() + '0')

    def baseOperations(self, sign):
        if sign == '*':
            sign = self.signList[0]
        elif sign == '/':
            sign = self.signList[1]
        elif sign == '+':
            sign = self.signList[2]
        elif sign == '-':
            sign = self.signList[3]

        if self.getTxt2()[-1:] == '=':
            self.setTxt2(self.getTxt1() + sign)

        if self.getTxt2()[-1:] == '(':
            pass
        elif self.getTxt2() != '' and self.getTxt2()[-1:] not in self.signList:
            self.setTxt2(self.getTxt2() + sign)
            self.setTxt1('0')
        elif self.getTxt2()[-1:] in self.signList:
            self.setTxt2(self.getTxt2()[:-1] + sign)
            self.setTxt1('0')
        self.allowNum = 1

    def sqrX(self):
        reqValue = str(int(self.getTxt1()) ** 2)
        self.setTxt2(self.getTxt2().removesuffix(self.getTxt1()))
        self.setTxt1(reqValue)
        self.setTxt2(self.getTxt2() + reqValue)
        self.allowNum = 0
        print('x\u00B2')

    def sqrRT(self):
        reqValue = str(round(sqrt(int(self.getTxt1())), 8))
        self.setTxt2(self.getTxt2().removesuffix(self.getTxt1()))
        self.setTxt1(reqValue)
        self.setTxt2(self.getTxt2() + reqValue)
        self.allowNum = 0
        print('\u221Ax')

    def xExp(self):
        reqValue = self.getTxt1()+'^'
        self.setTxt2(self.getTxt2().removesuffix(self.getTxt1()))
        self.setTxt1(reqValue)
        self.setTxt2(self.getTxt2() + reqValue)
        print('x\u02B8')

    def tenExp(self):
        tmpValue = self.getTxt2()[-1:]
        reqValue = '10^'
        if tmpValue in self.signList or tmpValue == '^':
            self.setTxt1(reqValue)
            self.setTxt2(self.getTxt2() + reqValue)
        elif tmpValue not in ('', '0'):
            self.setTxt1(reqValue)
            self.setTxt2(self.getTxt2() + '×' + reqValue)
        print('10\u036F')

    def logX(self):
        reqValue = str(log10(int(self.getTxt1())))
        self.setTxt2(self.getTxt2().removesuffix(self.getTxt1()))
        self.setTxt1(reqValue)
        self.setTxt2(self.getTxt2() + reqValue)
        print('logX')

    def lnX(self):
        reqValue = str(int(self.getTxt1()) ** 2)
        self.setTxt2(self.getTxt2().removesuffix(self.getTxt1()))
        self.setTxt1(reqValue)
        self.setTxt2(self.getTxt2() + reqValue)
        self.allowNum = 0
        print('lnX')

    def constantPi(self):
        inpValue = float(self.getTxt1())
        if inpValue == 0:
            self.setTxt1(str(pi))
            self.setTxt2(self.getTxt2() + '\u03C0')
        else:
            self.setTxt1(str(pi * inpValue))
            self.setTxt2(self.getTxt2() + '×' + '\u03C0')

    def numX(self):
        print('1/x')

    def openBracket1(self):
        reqStr = self.getTxt2()[-1:]
        if self.getTxt2() == '':
            self.setTxt2(self.getTxt2() + '(')
        elif reqStr[-1:] == '^':
            self.setTxt2(self.getTxt2() + '(')
        elif reqStr not in self.signList and reqStr != '(':
            self.setTxt1('0')
            self.setTxt2(self.getTxt2() + '×' + '(')
        else:
            self.setTxt2(self.getTxt2() + '(')

        self.endBracket += 1

    def openBracket2(self):
        # if self.trigEval != 0:
        #     reqList = self.getTxt2()[::-1].split('(')
        #     reqStr = reqList[0][::-1]
        #     value = str(eval(reqStr))
        #     for i in self.trigRatios:
        #         tmpList = self.getTxt2().split(i)
        #         if tmpList[-1].isdigit():
        #             reqLen = len(i)
        #             self.setTxt2(self.getTxt2()[:-len(reqStr)-reqLen]+value)
        #             break

        reqStr = self.getTxt2()
        if self.endBracket == 0:
            pass
        elif reqStr == '':
            pass
        elif reqStr[-1:] in self.signList:
            self.setTxt2(reqStr[:-1] + ')')
        else:
            self.setTxt2(reqStr + ')')

        if self.endBracket > 0:
            self.endBracket -= 1

    def negate(self):
        global tmpLst
        if int(self.getTxt1()) > 0:
            reqStr = int(self.getTxt1()) * -1
            for i in self.signList:
                tmpLst = self.getTxt2()[::-1].split(i, 1)
                if tmpLst[0].isdigit():
                    tmpLst[0] = f'{i}({str(reqStr)})'
                    break

            if not self.getTxt2().isdigit():
                tmpStr = tmpLst[1][::-1] + tmpLst[0]
            else:
                tmpStr = reqStr

            self.setTxt1(reqStr)
            self.setTxt2(tmpStr)

    def eConstant(self):
        print('Napier\'s Constant')

    def modX(self):
        print('|x|')

    def tenMultiplier(self):
        print('10x')

    def factorialNum(self):
        inpValue = eval(self.getTxt1())
        fact = inpValue
        try:
            for i in range(1, inpValue):
                fact *= i

            reqNum = len(self.getTxt2()) - len(self.getTxt1())
            if 'fact' in self.getTxt2():
                self.setTxt2(f'fact({self.getTxt2()})')
            else:
                self.setTxt2(self.getTxt2()[:reqNum] + f'fact({self.getTxt1()})')
        except TypeError:
            self.setTxt2('Bad Input!')

    def decimal(self):
        print('decimal')

    def clear(self):
        self.setTxt1('0')
        self.setTxt2('')
        self.endBracket = 0
        self.allowNum = 1

    def delLast(self):
        self.setTxt1(self.getTxt1()[:-1])

        if self.getTxt2()[-1:] not in self.signList:
            if self.getTxt2()[-1:] == ')':
                self.endBracket += 1
            elif self.getTxt2()[-1:] == '(':
                self.endBracket -= 1
            self.setTxt2(self.getTxt2()[:-1])

        if self.getTxt1() == '':
            self.setTxt1('0')

    def modulus(self):
        pass

    def sin(self):
        if self.getTxt2() == '':
            self.setTxt2('sin(')
        elif self.getTxt2()[-1:] == '(':
            self.setTxt2(self.getTxt2() + 'sin(')
        elif self.getTxt2()[-1:] == '=':
            self.setTxt1('0')
            self.setTxt2('sin(')
        elif self.getTxt2()[-1:] not in self.signList:
            self.setTxt2(self.getTxt2() + '×' + 'sin(')
        else:
            self.setTxt2(self.getTxt2() + 'sin(')

        self.trigEval += 1
        self.endBracket += 1

    def cos(self):
        if self.getTxt2() == '':
            self.setTxt2('cos(')
        elif self.getTxt2()[-1:] == '(':
            self.setTxt2(self.getTxt2() + 'cos(')
        elif self.getTxt2()[-1:] == '=':
            self.setTxt1('0')
            self.setTxt2('cos(')
        elif self.getTxt2()[-1:] not in self.signList:
            self.setTxt2(self.getTxt2() + '×' + 'cos(')
        else:
            self.setTxt2(self.getTxt2() + 'cos(')

        self.trigEval += 1
        self.endBracket += 1

    def tan(self):
        if self.getTxt2() == '':
            self.setTxt2('tan(')
        elif self.getTxt2()[-1:] == '(':
            self.setTxt2(self.getTxt2() + 'tan(')
        elif self.getTxt2()[-1:] == '=':
            self.setTxt1('0')
            self.setTxt2('tan(')
        elif self.getTxt2()[-1:] not in self.signList:
            self.setTxt2(self.getTxt2() + '×' + 'tan(')
        else:
            self.setTxt2(self.getTxt2() + 'tan(')

        self.trigEval += 1
        self.endBracket += 1

    def cot(self):
        if self.getTxt2() == '':
            self.setTxt2('1/tan(')
        elif self.getTxt2()[-1:] == '(':
            self.setTxt2(self.getTxt2() + '1/tan(')
        elif self.getTxt2()[-1:] == '=':
            self.setTxt1('0')
            self.setTxt2('1/tan(')
        elif self.getTxt2()[-1:] not in self.signList:
            self.setTxt2(self.getTxt2() + '×' + '1/tan(')
        else:
            self.setTxt2(self.getTxt2() + '1/tan(')

        self.trigEval += 1
        self.endBracket += 1

    def sec(self):
        if self.getTxt2() == '':
            self.setTxt2('1/cos(')
        elif self.getTxt2()[-1:] == '(':
            self.setTxt2(self.getTxt2() + '1/cos(')
        elif self.getTxt2()[-1:] == '=':
            self.setTxt1('0')
            self.setTxt2('1/cos(')
        elif self.getTxt2()[-1:] not in self.signList:
            self.setTxt2(self.getTxt2() + '×' + '1/cos(')
        else:
            self.setTxt2(self.getTxt2() + '1/cos(')

        self.trigEval += 1
        self.endBracket += 1

    def cosec(self):
        if self.getTxt2() == '':
            self.setTxt2('1/sin(')
        elif self.getTxt2()[-1:] == '(':
            self.setTxt2(self.getTxt2() + '1/sin(')
        elif self.getTxt2()[-1:] == '=':
            self.setTxt1('0')
            self.setTxt2('1/sin(')
        elif self.getTxt2()[-1:] not in self.signList:
            self.setTxt2(self.getTxt2() + '×' + '1/sin(')
        else:
            self.setTxt2(self.getTxt2() + '1/sin(')

        self.trigEval += 1
        self.endBracket += 1

    def equalsTo(self):
        inpValue = self.getTxt2()
        valList = list(inpValue)

        for i in range(len(valList)):  # Changing The Symbols For eval(); To Run It Smoothly
            if valList[i] == self.signList[0]:
                valList[i] = '*'

            elif valList[i] == self.signList[1]:
                valList[i] = '/'

            elif valList[i] == self.signList[2]:
                valList[i] = '+'

            elif valList[i] == self.signList[3]:
                valList[i] = '-'

            elif valList[i] == '^':
                valList[i] = '**'

            elif valList[i] == '\u03C0':
                valList[i] = 'pi'

        inpValue = ''.join(valList)
        if 'fact' in inpValue:
            inpValue = inpValue.replace('fact', 'factorial')

        while self.trigEval != 0:
            for i in self.trigRatios:
                if i in inpValue:
                    if i != 'sec(':
                        inpValue = inpValue.replace(i, f'{i}radians(')
                        inpValue += ')'
                        self.trigEval -= 1


        if inpValue[-1:] in self.signList:
            self.setTxt2(self.getTxt2()[:-1])
        else:
            if inpValue[-1:] == '=':
                self.setTxt2(self.getTxt2())
            else:
                self.setTxt2(self.getTxt2() + '=')

        while self.endBracket != 0:
            if self.getTxt2()[-1:] == '=':
                self.setTxt1('0')
                self.setTxt2(self.getTxt2()[:-1] + ')=')
            else:
                self.setTxt1('0')
                self.setTxt2(self.getTxt2() + ')=')

            if inpValue[-1:] == '=':
                inpValue = inpValue[:-1] + ')='
            else:
                inpValue += ')='

            self.endBracket -= 1

        if inpValue[-1:] in self.signList:
            self.setTxt1(round(eval(inpValue[:-1]), 8))
        elif inpValue[-1:] == '=':
            self.setTxt1(round(eval(inpValue[:-1]), 8))
        else:
            self.setTxt1(round(eval(inpValue), 8))

        if self.getTxt1()[-2:] == '.0':
            self.setTxt1(self.getTxt1()[:-2])

        self.allowNum = 1


root = Tk()
obj = myProject()
root.mainloop()
