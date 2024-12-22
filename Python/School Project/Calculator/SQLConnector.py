from tkinter import *


class myActivity:
    def __init__(self):
        self.root = root
        self.root.geometry('425x544+450+100')
        self.root.title('Activity')
        self.root.resizable(False, False)

        lbl = Label(root, bd=3, relief=RIDGE, fg='magenta', text='Login 3/15/2022 8:36pm',
                    font=('comic sans ms', 16, 'bold'))
        lbl.place(relx=0, rely=0, relwidth=1, relheight=0.2)
        lbl = Label(root, bd=3, relief=RIDGE, fg='magenta', text='Login 3/16/2022 4:56pm',
                    font=('comic sans ms', 16, 'bold'))
        lbl.place(relx=0, rely=0.2, relwidth=1, relheight=0.2)
        lbl = Label(root, bd=3, relief=RIDGE, fg='magenta', text='Login 3/17/2022 4:39pm',
                    font=('comic sans ms', 16, 'bold'))
        lbl.place(relx=0, rely=0.4, relwidth=1, relheight=0.2)
        lbl = Label(root, bd=3, relief=RIDGE, fg='magenta', text='Login 3/18/2022 3:56pm',
                    font=('comic sans ms', 16, 'bold'))
        lbl.place(relx=0, rely=0.6, relwidth=1, relheight=0.2)
        lbl = Label(root, bd=3, relief=RIDGE, fg='magenta', text='Login 3/19/2022 8:32pm',
                    font=('comic sans ms', 16, 'bold'))
        lbl.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)


root = Tk()
obj = myActivity()
root.mainloop()
