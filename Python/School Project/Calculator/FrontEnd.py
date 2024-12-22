from tkinter import *
from os import getcwd, chdir, system


class frontEnd:
    def __init__(self):
        self.root = root
        root.geometry('500x500+360+140')
        root.title('Home Page | Student Toolkit')
        root.resizable(False, False)

        # ======== Variables ========
        userName = StringVar()
        password = StringVar()
        self.status = 'Connected!'

        # ======== Frames ========
        mainFrame = Frame(root, bg='black', bd=4, relief=RIDGE)
        mainFrame.place(x=0, y=0, relheight=0.2, relwidth=1)

        loginFrame = Frame(root, bg='black', bd=4, relief=RIDGE)
        loginFrame.place(x=0, rely=0.2, relheight=0.8, relwidth=0.6)

        menuFrame = Frame(root, bg='black', bd=4, relief=RIDGE)
        menuFrame.place(relx=0.6, rely=0.2, relheight=0.8, relwidth=0.4)

        # ======== Labels ========
        headLabel = Label(mainFrame, bg='cyan', text='Welcome', font=('comic sans ms', 32, 'bold'))
        headLabel.place(x=0, y=0, relheight=1, relwidth=1)

        colLabel = Label(loginFrame, bg='blue')
        colLabel.place(x=0, y=0, relheight=1, relwidth=1)
        colLabel = Label(menuFrame, bg='blue')
        colLabel.place(x=0, y=0, relheight=1, relwidth=1)

        usrLblFrame = LabelFrame(loginFrame, bg='black')
        usrLblFrame.place(relx=0.1, rely=0.05, relheight=0.1, relwidth=0.8)

        userLabel = Label(usrLblFrame, fg='white', bg='black', font=('comic sans ms', 20, 'bold'), text='User Name')
        userLabel.place(relx=0, rely=0, relheight=1, relwidth=1)

        userEntry = Entry(loginFrame, textvariable=userName, font=('comic sans ms', 20, 'bold'))
        userEntry.place(relx=0.1, rely=0.2, relheight=0.1, relwidth=0.8)

        passLblFrame = LabelFrame(loginFrame, bg='black')
        passLblFrame.place(relx=0.1, rely=0.35, relheight=0.1, relwidth=0.8)

        passLabel = Label(passLblFrame, fg='white', bg='black', font=('comic sans ms', 20, 'bold'), text='Password')
        passLabel.place(relx=0, rely=0, relheight=1, relwidth=1)

        passEntry = Entry(loginFrame, textvariable=password, font=('comic sans ms', 20, 'bold'))
        passEntry.place(relx=0.1, rely=0.5, relheight=0.1, relwidth=0.8)

        statusFrame = Label(loginFrame, text=self.status, font=('comic sans ms', 20, 'bold'), fg='green', bg='blue')
        statusFrame.place(relx=0.1, rely=0.85, relheight=0.1, relwidth=0.8)

        # ======== Buttons ========
        loginBtn = Button(loginFrame, bg='light grey', text='Login', font=('comic sans ms', 20, 'bold'))
        loginBtn.place(relx=0.1, rely=0.65, relheight=0.15, relwidth=0.8)

        calcBtn = Button(menuFrame, bg='light grey', text='Calculator', font=('comic sans ms', 20, 'bold'),
                         command=self.calc)
        calcBtn.place(relx=0.1, rely=0.1, relheight=0.2, relwidth=0.8)

        gameBtn1 = Button(menuFrame, bg='light grey', text='Game-Memory', font=('comic sans ms', 16, 'bold'),
                          command=self.game1)
        gameBtn1.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)

        gameBtn2 = Button(menuFrame, bg='light grey', text='Game-Tiles', font=('comic sans ms', 20, 'bold'),
                          command=self.game2)
        gameBtn2.place(relx=0.1, rely=0.5, relheight=0.2, relwidth=0.8)

        activityBtn = Button(menuFrame, bg='light grey', text='Activity', font=('comic sans ms', 20, 'bold'),
                             command=self.activity)
        activityBtn.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.8)

    def calc(self):
        chdir(getcwd())
        system("python Calculator.py")

    def game1(self):
        chdir(getcwd())
        system("python Memory.py")

    def game2(self):
        chdir(getcwd())
        system("python Tiles.py")

    def activity(self):
        chdir(getcwd())
        system("python SQLConnector.py")


root = Tk()
obj = frontEnd()
root.mainloop()
