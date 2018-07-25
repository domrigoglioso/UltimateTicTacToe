from UltimateBoard import *
from tkinter import *
from tkinter import ttk

# root = Tk()
# 1)
# frame = Frame(root)
# labelText = StringVar()
# label = Label(frame, textvariable=labelText)
# button = Button(frame, text="Click")
# labelText.set("Label")
# label.pack()
# button.pack()
# frame.pack()

# 2) Pack
# frame = Frame(root)
# Label(frame, text="Bunch of buttons").pack()
# Button(frame, text="B1").pack(side=LEFT, fill=Y)
# Button(frame, text="B2").pack(side=TOP, fill=X)
# Button(frame, text="B3").pack(side=RIGHT, fill=X)
# Button(frame, text="B4").pack(side=LEFT, fill=X)
# frame.pack()

# 3) Grid
# Sticky is how the widget expands, N, NE, NW, W, E, SE, ...
# Label(root, text="Label1").grid(row=0, sticky=W, padx=4)
# Entry(root).grid(row=0, column=1, sticky=E, pady=4)
# Label(root, text="Labe2").grid(row=1, sticky=W, padx=4)
# Entry(root).grid(row=1, column=1, sticky=E, pady=4)
# Button(root, text="Button").grid(row=3)

# 4)
# Label(root, text="Description").grid(row=0, column=0, sticky=W)
# Entry(root, width=50).grid(row=0, column=1)
# Button(root, text="Submit").grid(row=0, column=8)
# Label(root, text="Quality").grid(row=1, column=0, sticky=W)
# Radiobutton(root, text="New", value=1).grid(row=2, column=0, sticky=W)
# Radiobutton(root, text="Good", value=2).grid(row=3, column=0, sticky=W)
# Radiobutton(root, text="Poor", value=3).grid(row=4, column=0, sticky=W)
# Radiobutton(root, text="Shit", value=4).grid(row=5, column=0, sticky=W)
# Label(root, text="Benefits").grid(row=1, column=1, sticky=W)
# Checkbutton(root, text="Free Shipping").grid(row=2, column=1, sticky=W)
# Checkbutton(root, text="Bonus").grid(row=3, column=1, sticky=W)

# 5) Events
# def get_sum(event):
#     num1 = int(num1Entry.get())
#     num2 = int(num2Entry.get())
#     sum = num1 + num2
#     sumEntry.delete(0, "end")
#     sumEntry.insert(0, sum)
#
# root = Tk()
# num1Entry = Entry(root)
# num1Entry.pack(side=LEFT)
# Label(root, text="+").pack(side=LEFT)
# num2Entry = Entry(root)
# num2Entry.pack(side=LEFT)
# equalButton = Button(root, text="=")
# # Event is left mouse click (button 1), function is get_sum
# equalButton.bind("<Button-1>", get_sum)
# equalButton.pack(side=LEFT)
#
# sumEntry = Entry(root)
# sumEntry.pack(side=LEFT)
# root.mainloop()


class MiniBoardFrame:
    def __init__(self, root, mb, bx, by):
        self.mb_frame = Frame(root)
        self.text = [[StringVar() for x in range(3)] for y in range(3)]
        self.button = [[Button(self.mb_frame, textvariable=self.text[x][y],
                               height=5, width=10, bg="PaleTurquoise1")
                        for x in range(3)] for y in range(3)]
        for y in range(3):
            for x in range(3):
                self.text[x][y].set(mb.box_to_letter(x, y))
                self.button[x][y].grid(row=y, column=x, sticky=W)
        # self.mb_frame.grid(row=bx, column=by, sticky=W)
        self.paddingX = Label(root, height=2, width=4)
        self.paddingX.grid(row=by*2, column=bx*2+1, sticky=W)
        self.paddingY = Label(root, height=2, width=4)
        self.paddingY.grid(row=by*2+1, column=bx*2, sticky=W)
        self.mb_frame.grid(row=by*2, column=bx*2, sticky=W)

    def set_valid(self):
        for y in range(3):
            for x in range(3):
                self.button[x][y].configure(bg="PaleGreen1")

    def get_frame(self):
        return self.mb_frame


class UltimateBoardFrame(Frame):
    def __init__(self, root, ub):
        self.ub_frame = Frame(root)
        self.mb_frames = [[MiniBoardFrame(self.ub_frame, ub.boards[x][y],
                                          x, y) for x in
                           range(3)] for y in range(3)]
        self.ub_frame.pack()

    def get_frame(self):
        return self.ub_frame


root = Tk()
# m1 = MiniBoard()
# m1.do_move(0, 0, -1)
# m1.do_move(1, 1, 1)
# mb = MiniBoardFrame(root, m1, 0, 0)
# mb.set_valid()
# f = mb.get_frame()
u1 = UltimateBoard()
ub = UltimateBoardFrame(root, u1)
root.mainloop()






