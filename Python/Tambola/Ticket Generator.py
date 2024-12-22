from tkinter import *

root = Tk()

root = root
root.geometry("502x530+433+133")
root.title("Tambola")

bgc = "#074463"

F2 = LabelFrame(self.root, text="", bg=bgc, bd=10, relief=GROOVE)
F2.place(x=0, y=421, relwidth=1)

gnr_btn = Button(F2, text="Generate", bd=8, font="arial 28 bold", bg="gold", width=10).pack(side=LEFT)
run_btn = Button(F2, text="Play", bd=8, font="arial 28 bold", bg="gold", width=10).pack(side=RIGHT)

root.mainloop()