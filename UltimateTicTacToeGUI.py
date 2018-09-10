from UltimateBoard import *
from tkinter import *
import Controller
import time

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


# Used to turn -1 to O, and X to 1
def int_to_letter(player):
    if player == 1:
        return "X"
    else:
        return "O"


class MiniBoardFrame:
    def __init__(self, root, mb, bx, by):
        self.mb = mb
        self.mb_frame = Frame(root)
        self.text = [[StringVar() for x in range(3)] for y in range(3)]
        self.button = [[Button(self.mb_frame, textvariable=self.text[y][x],
                               height=5, width=10, bg="PaleGreen1")
                        for x in range(3)] for y in range(3)]
        for y in range(3):
            for x in range(3):
                self.text[y][x].set(mb.box_to_letter(x, y))
                self.button[y][x].grid(row=y, column=x, sticky=W)
        self.mb_frame.grid(row=by, column=bx, sticky=W, padx=20, pady=20)

    def set_valid(self):
        for y in range(3):
            for x in range(3):
                self.button[y][x].configure(bg="PaleGreen1")

    def set_won(self):
        for y in range(3):
            for x in range(3):
                if self.mb.finished == 1:
                    self.button[y][x].configure(bg="pale goldenrod")
                elif self.mb.finished == -1:
                    self.button[y][x].configure(bg="PaleVioletRed1")
                elif self.mb.finished == 10:
                    self.button[y][x].configure(bg="PaleTurquoise4")
                else:
                    self.button[y][x].configure(bg="PaleTurquoise1")

    def set_invalid(self):
        for y in range(3):
            for x in range(3):
                if self.mb.finished == 1:
                    self.button[y][x].configure(bg="pale goldenrod")
                elif self.mb.finished == -1:
                    self.button[y][x].configure(bg="PaleVioletRed1")
                elif self.mb.finished == 10:
                    self.button[y][x].configure(bg="PaleTurquoise4")
                else:
                    self.button[y][x].configure(bg="PaleTurquoise1")

    def get_frame(self):
        return self.mb_frame


class UltimateBoardFrame():
    def __init__(self, root: Tk, ub: UltimateBoard):
        self.ub_frame = Frame(root)
        self.root = root
        self.ub = ub
        # MiniBoards
        self.mb_frames = [[MiniBoardFrame(self.ub_frame, ub.boards[y][x],
                                          x, y) for x in
                           range(3)] for y in range(3)]
        self.ub_frame.grid(row=0, column=0, sticky=W)
        # Side Menu: Opponent type, turns played, current player
        # Opponent 1
        self.optionsFrame = Frame(self.ub_frame)
        self.optionsFrame.grid(row=0, column=4, sticky=W)
        self.opp1 = StringVar()
        self.opp1.set("Player 1 Type")
        self.opponent1Option = OptionMenu(self.optionsFrame, self.opp1, "Human",
                                          "Random AI", "Mini-Max AI",
                                          "Monte Carlo AI", "Multi-Armed "
                                                            "Bandit AI")
        self.opponent1Option.config(width=19)
        self.opponent1Option.grid(row=0, column=0, sticky=W)
        # Opponent 2
        self.opp2 = StringVar()
        self.opp2.set("Player 2 Type")
        self.opponent2Option = OptionMenu(self.optionsFrame, self.opp2, "Human",
                                          "Random AI", "Mini-Max AI",
                                          "Monte Carlo AI", "Multi-Armed "
                                                            "Bandit AI")
        self.opponent2Option.config(width=19)
        self.opponent2Option.grid(row=1, column=0, sticky=W)
        # Start Button
        self.startButton = Button(self.optionsFrame, text="Start", width=21)
        self.startButton.grid(row=2, column=0, sticky=W)
        self.startButton.bind("<Button-1>", lambda event: self.start_game())
        # Reset
        self.startButton = Button(self.optionsFrame, text="Reset", width=21)
        self.startButton.grid(row=3, column=0, sticky=W)
        self.startButton.bind("<Button-1>", lambda event: self.reset())
        # Current Player
        self.currentPlayer = StringVar()
        self.currentPlayer.set("Current Player: " +
                               int_to_letter(self.ub.currentPlayer))
        self.currentPlayerLabel = Label(self.optionsFrame,
                                        textvar=self.currentPlayer)
        self.currentPlayerLabel.grid(row=4, column=0, sticky=W)
        # Turns Elapsed
        self.turnsElapsed = StringVar()
        self.turnsElapsed.set("Turns Elapsed: " + str(self.ub.turnsElapsed))
        self.turnsElapsedLabel = Label(self.optionsFrame,
                                       textvar=self.turnsElapsed)
        self.turnsElapsedLabel.grid(row=5, column=0, sticky=W)

        self.gameTypes = ["Human-Human", "Human-AI", "AI-AI", "AI-Human"]
        # TODO: Change gametype to change based on input.
        self.player = {1: "Random", -1: "Minimax"}
        # self.disable_buttons()

    def get_frame(self):
        return self.ub_frame

    def disable_buttons(self):
        for by in range(3):
            for bx in range(3):
                for iy in range(3):
                    for ix in range(3):
                        # equalButton.bind("<Button-1>", get_sum)
                        self.mb_frames[by][bx].button[iy][ix].config(
                            state="disabled")

    def setup_buttons(self):
        for by in range(3):
            for bx in range(3):
                for iy in range(3):
                    for ix in range(3):
                        # equalButton.bind("<Button-1>", get_sum)
                        self.mb_frames[by][bx].button[iy][ix].bind(
                            "<Button-1>", lambda event, bx=bx, by=by, ix=ix,
                                                 iy=iy: self.user_move(bx, by,
                                                                     ix, iy))

    def user_move(self, bx, by, ix, iy):
        # self.mb_frames[self.ub.lastPlayedY][self.ub.lastPlayedX].set_invalid()
        Controller.move(self, bx, by, ix, iy)
        self.root.update()
        self.next_move()

    def start_game(self):
        if self.player[1] == "Human" or self.player[-1] == "Human":
            self.setup_buttons()
        self.next_move()
        self.startButton.config(relief=RAISED)
        self.root.update()

    def next_move(self):
        if self.ub.finished != 0:
            return
        if self.player[self.ub.currentPlayer] == "Human":
            return
        self.ai_move()

    def ai_move(self):
        if self.player[self.ub.currentPlayer] == "Random":
            Controller.random_move(self)
        if self.player[self.ub.currentPlayer] == "Minimax":
            Controller.minimax_move(self)

        if self.player[1] != "Human" and self.player[-1] != "Human":
            self.root.after(50, self.root.update())
            self.next_move()
        else:
            self.root.after(200, self.next_move())

    def set_valid_boards(self):
        if self.ub.lastPlayedX == -1:
            for y in range(3):
                for x in range(3):
                    self.mb_frames[y][x].set_invalid()
        else:
            self.mb_frames[self.ub.lastPlayedY][self.ub.lastPlayedX]\
                .set_invalid()

    def update_board(self, bx, by, ix, iy):
        # self.set_valid_boards()
        # Update letters in boxes
        self.mb_frames[by][bx].text[iy][ix].set(self.ub.boards[by][bx]
                                                .box_to_letter(ix, iy))

        # Check if box was won
        if self.ub.boards[by][bx].finished != 0:
            self.mb_frames[by][bx].set_won()

        # Check which boxes are valid
        if self.ub.finished == 0:
            if self.ub.lastPlayedX == -1:
                for y in range(3):
                    for x in range(3):
                        if self.ub.boardStates[y][x] == 0:
                            self.mb_frames[y][x].set_valid()
            else:
                self.mb_frames[self.ub.lastPlayedY][self.ub.lastPlayedX].\
                    set_valid()

        self.turnsElapsed.set("Turns Elapsed: " + str(self.ub.turnsElapsed))
        self.currentPlayer.set("Current Player: " +
                               int_to_letter(self.ub.currentPlayer))
        # self.mb_frames[self.ub.lastPlayedY][self.ub.lastPlayedX].set_valid()

    def set_new_board(self):
        # Check which boxes are valid
        if self.ub.finished == 0:
            if self.ub.lastPlayedX == -1:
                for y in range(3):
                    for x in range(3):
                        self.mb_frames[y][x] = \
                            MiniBoardFrame(self.ub_frame, self.ub.boards[y][x],
                                           x, y)
            else:
                self.mb_frames[self.ub.lastPlayedY][self.ub.lastPlayedX]. \
                    set_valid()

        self.turnsElapsed.set("Turns Elapsed: " + str(self.ub.turnsElapsed))
        self.currentPlayer.set("Current Player: " +
                               int_to_letter(self.ub.currentPlayer))

    def reset(self):
        self.ub = UltimateBoard()
        self.set_new_board()


if __name__ == "__main__":
    root = Tk()
    # m1 = MiniBoard()
    # m1.do_move(0, 0, -1)
    # m1.do_move(1, 1, 1)
    # mb = MiniBoardFrame(root, m1, 0, 0)
    # mb.set_valid()
    # f = mb.get_frame()
    u1 = UltimateBoard()
    # for i in range(100):
    #     if u1.lastPlayedX != -1:
    #         bx = u1.lastPlayedX
    #         by = u1.lastPlayedY
    #         rx = random.randint(0, 2)
    #         ry = random.randint(0, 2)
    #         u1.do_move4(bx, by, rx, ry)
    #     else:
    #         rx = random.randint(0, 8)
    #         ry = random.randint(0, 8)
    #         # print(rx, ry)
    #         u1.do_move2(rx, ry)
    # for i in range(40):
    #     u1.random_move()
    # print(u1.boards[0][0].count_occurrences(2, 1))
    # print(u1.boards[0][0].count_occurrences(2, -1))
    # print(u1.boards[0][0].count_occurrences(1, 1))
    # print(u1.boards[0][0].count_occurrences(1, -1))
    # print(u1.boards[0][0].eval_mini())
    # print(u1.get_board_value())
    # u1.do_move4(1, 1, 1, 1)
    # u1.do_move4(1, 1, 2, 0)
    # u1.do_move4(2, 0, 1, 1)
    # u1.do_move4(1, 1, 1, 0)
    # u1.do_move4(1, 0, 1, 1)
    # u1.do_move4(0, 0, 1, 1)
    # u1.do_move4(1, 1, 0, 0)
    # print(u1.lastPlayedX)
    ub = UltimateBoardFrame(root, u1)

    # ub.mainloop()
    root.mainloop()
    # ub.next_move()

    # print(u1)
    # print(u1.finished)
    # mb = MiniBoardFrame(root, u1.boards[2][0], 0, 0)
    # m2 = MiniBoard()
    # m2.do_move(2, 1, 1)
    # print(m2)
    # print(m2.state[1][2])
    # mb = MiniBoardFrame(root, m2, 0, 0)
    # root.mainloop()






