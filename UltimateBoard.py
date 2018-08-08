from MiniBoard import MiniBoard
import random
import copy
from collections import namedtuple
# TwoPoint is for holding the location of a coordinate (innerX, innerY)
# within the MiniBoard at location (boardX, boardY)
TwoPoint = namedtuple('TwoPoint', 'boardX boardY innerX innerY')


class UltimateBoard:

    def __init__(self):
        self.boards = [[MiniBoard() for x in range(3)] for y in
                       range(3)]
        self.boardStates = [[0 for x in range(3)] for y in range(3)]
        self.turnsElapsed = 0
        # -1 for a lastPlayed coordinate denotes any move is valid.
        self.lastPlayedX = -1
        self.lastPlayedY = -1
        self.currentPlayer = 1
        self.finished = 0
        self.lastMove = {}

    # Precondition: x and y are each from 0 to 8
    # Postcondition: Returns a named tuple of 4 numbers, each from 0 to 2.
    # The first two numbers are the x and y coordinates of the MiniBoard that
    # the move would be played in. The last two numbers are the x and y
    # coordinates within that respective box.
    # Note: It's two because it converts two coordinates (into four).
    @staticmethod
    def convert_coords_two(x, y):
        innerX = x % 3
        innerY = y % 3
        boardX = x // 3
        boardY = y // 3
        coord = TwoPoint(boardX, boardY, innerX, innerY)
        return coord

    # Precondition: Each four inputs are from 0 to 2. (bx, by) is the
    # location of a MiniBoard. (ix, iy) is the location of a move within that
    # MiniBoard.
    # Postcondition: Returns a tuple of 2 numbers. This is the (x, y)
    # coordinates that the move at MiniBoard (bx, by) at (ix, iy) within that
    # MiniBoard would be located in a larger 9x9 representation.
    # Note: It's four because it converts four coordinates (into two).
    @staticmethod
    def convert_coords_four(bx, by, ix, iy):
        x = bx*3+ix
        y = by*3+iy
        return x, y

    # Moves on to the next turn
    # x, y are between 0 and 2. They represent the last place in a MiniBoard
    # a move was played.
    def proceed_turn(self, boardX, boardY, innerX, innerY):
        self.turnsElapsed += 1
        self.lastPlayedX = innerX
        self.lastPlayedY = innerY
        self.boardStates[boardY][boardX] = \
            self.boards[boardY][boardX].check_win()
        if self.boardStates[innerY][innerX] != 0:
            self.lastPlayedX = -1
            self.lastPlayedY = -1
        self.currentPlayer *= -1
        self.lastMove = (boardX, boardY, innerX, innerY)
        self.finished = self.check_win()

    # Precondition: x and y are between 0 and 8
    # Makes a move on the board and moves on to the next turn.
    def do_move_dirty2(self, x, y):
        c = UltimateBoard.convert_coords_two(x, y)
        self.boards[c.boardY][c.boardX].do_move_dirty(c.innerX, c.innerY,
                                                      self.currentPlayer)
        self.proceed_turn(c.boardX, c.boardY, c.innerX, c.innerY)

    # Precondition: boardX, boardY, innerX, innerY are between 0 and 2
    # Makes a move on the board and moves on to the next turn.
    def do_move_dirty4(self, boardX, boardY, innerX, innerY):
        self.boards[boardY][boardX].do_move_dirty(innerX, innerY,
                                                  self.currentPlayer)
        self.proceed_turn(boardX, boardY, innerX, innerY)

    # Precondition: x and y are between 0 and 8
    # Makes a move on the board and moves on to the next turn if (x, y) is a
    # a valid U. T-T-T move, otherwise nothing happens.
    def do_move2(self, x, y):
        c = UltimateBoard.convert_coords_two(x, y)
        if self.is_valid(c.boardX, c.boardY, c.innerX, c.innerY):
            self.boards[c.boardY][c.boardX].do_move(c.innerX, c.innerY,
                                                    self.currentPlayer)
            self.proceed_turn(c.boardX, c.boardY, c.innerX, c.innerY)

    # Precondition: boardX, boardY, innerX, innerY are between 0 and 2
    # Makes a move on the board and moves on to the next turn.
    def do_move4(self, boardX, boardY, innerX, innerY):
        if self.is_valid(boardX, boardY, innerX, innerY):
            self.boards[boardY][boardX].do_move(innerX, innerY,
                                                self.currentPlayer)
            self.proceed_turn(boardX, boardY, innerX, innerY)

    # Checks if a move in MiniBoard (bx, by) at (ix, iy) is valid. A move is
    # valid if it meets the following criteria:
    #   1) The game has not ended
    #   2) The MiniBoard has not been "finished" (won or completely filled)
    #   3)The MiniBoard location is at the location of the last played inner
    #     move or the previous inner move landed in a "finished" board
    def is_valid(self, bx, by, ix, iy):
        return self.finished == 0 and self.boardStates[by][bx] == 0 \
               and ((self.lastPlayedX == bx and self.lastPlayedY == by)
                    or self.lastPlayedX == -1) and \
               self.boards[by][bx].is_valid(ix, iy)

    # Return -1, or 1 if O or X has won the tic-tac-toe game, respectively.
    # Return 0 if the game has not been won.
    # Return 10 if the game is tied.
    def check_win(self):
        cols = self.check_columns()
        rows = self.check_rows()
        dia = self.check_diagonals()
        if cols != -1:
            return self.boardStates[0][cols]
        elif rows != -1:
            return self.boardStates[rows][0]
        elif dia:
            return self.boardStates[1][1]
        elif self.check_filled():
            return 10
        return 0

    # Return the row number of a winning row of the tic-tac-toe game
    # -1 if there is no winner in a row
    def check_rows(self):
        # If the sum of the numbers in a column add up to 3 or -3,
        # then X (1) or O (-1), respectively, has won
        # Col 0
        for y in range(3):
            if abs(self.boardStates[y][0] + self.boardStates[y][1] +
                   self.boardStates[y][2]) == 3:
                return y
        return -1

    # Return the column number of a winning row of the large tic-tac-toe game
    # -1 if there is no winner in a column
    def check_columns(self):
        # If the sum of the numbers in a column add up to 3 or -3,
        # then X (1) or O (-1), respectively, has won
        # Col 0
        for x in range(3):
            if abs(self.boardStates[0][x] + self.boardStates[1][x] +
                   self.boardStates[2][x]) == 3:
                return x
        return -1

    # Return true if any of the diagonals of the tic-tac-toe game
    # have a 3 in a row of a single player
    def check_diagonals(self):
        if abs(self.boardStates[0][0] + self.boardStates[1][1] +
               self.boardStates[2][2]) == 3:
            return True
        elif abs(self.boardStates[2][0] + self.boardStates[1][1] +
                 self.boardStates[0][2]) == 3:
            return True
        return False

    # Return a list of valid moves from the current board position
    # A valid move is returned as a tuple
    # (valid_board_x, valid_board_y, valid_inner_x, valid_inner_y)
    def get_valid_moves(self):
        moves = []
        for by in range(3):
            for bx in range(3):
                for iy in range(3):
                    for ix in range(3):
                        if self.is_valid(bx, by, ix, iy):
                            moves.append(TwoPoint(bx, by, ix, iy))
        return moves

    # Takes a list of lists, and turns it into one list
    # l is a list of lists.
    @staticmethod
    def flatten(l):
        flat = []
        for sublist in l:
            for item in sublist:
                flat.append(item)
        return flat

    # Return true if all the boxes are filled and false otherwise
    # False otherwise
    def check_filled(self):
        for y in range(3):
            for x in range(3):
                if self.boardStates[y][x] == 0:
                    return False
        return True

    # Does a random valid move
    def random_move(self):
        if self.finished != 0:
            return
        moves = self.get_valid_moves()
        num_moves = len(moves)
        r = random.randint(0, len(moves)-1)
        move = moves[r]
        self.do_move4(move.boardX, move.boardY, move.innerX, move.innerY)

    def __str__(self):
        # line = "\n|---|---|---|\t|---|---|---|\t|---|---|---|\n"
        st = ""
        for y in range(3):
            for inner_y in range(3):
                for x in range(3):
                    st = st + self.boards[y][x].print_row(inner_y) + "\t"
                st = st + "\n"
                # st = st + line
            st = st + "\n"
        st = st + "Current Player: " + str(self.currentPlayer) \
             + "\t Last Played: (" \
             + str(self.lastPlayedX) + ", " + str(self.lastPlayedY) \
             + ") \tTurns Elapsed: " + str(self.turnsElapsed)
        return st


# print(UltimateBoard.convert_coords_four(2, 2, 2, 2))
# m = MiniBoard()
# m.do_move_dirty(0, 0)
# m.do_move_dirty(1, 0)
# m.do_move(1, 2)
# n = copy.deepcopy(m)
# print(m)
# n.do_move(2, 2)
#
# q = n.get_valid_moves()
# n.do_move(0, 1)
# n.do_move(2, 1)
# n.do_move(1, 1)
# n.do_move(0, 2)
# n.do_move(2, 0)
# print(n)
# win = n.check_win()
# print(win)
# u1 = UltimateBoard()
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


# for y in range(3):
#     for x in range(3):
#         print("\t" + str(u1.boardStates[x][y]))
# u1.do_move2(6, 1)
# print(UltimateBoard.convert_coords_two(6, 1))
# u1.do_move_dirty2(5, 5)
# u1.do_move4(0, 0, 0, 0)
# u1.do_move4(2, 2, 1, 1)
# u1.do_move4(1, 1, 0, 2)
# u1.do_move4(0, 2, 2, 0)

# print(u1)
# print(u1.check_win())
# print(u1.get_valid_moves())
