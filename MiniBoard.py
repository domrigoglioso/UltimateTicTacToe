

class MiniBoard:
    def __init__(self):
        # State is a 2d array depicting where the X's and O's are in the board
        self.state = [[0 for x in range(3)] for y in range(3)]
        # currentPlayer denotes which players turn it currently is.
        # 1 for player X, -1 for player O
        self.currentPlayer = 1
        # finished denotes if the game is finished.
        # It is 0 if the game is ongoing, 1 if X has won the game,
        # -1 if O has won the game, and 10 if a tie.
        self.finished = 0
        # turnsElapsed is the number of turns the game has gone on for.
        self.turnsElapsed = 0
        # lastPlayed is the coordinates of the last box played.
        self.lastPlayed = (-1, -1)
        # The value of this board according to the heuristic found below
        self.score = 0

    def __str__(self):
        line = "\n|---|---|---|\n"
        st = " -----------\n"
        for y in range(3):
            st = st + self.print_row(y)
            if y != 2:
                st = st + line
            else:
                st = st + "\n -----------"
        return st

    # Prints row y
    def print_row(self, y):
        st = ""
        for x in range(3):
            if x == 0:
                st = st + "| " + self.box_to_letter(x, y) + " | "
            if x == 1:
                st = st + self.box_to_letter(x, y)
            if x == 2:
                st = st + " | " + self.box_to_letter(x, y) + " | "
        return st

    # Displays X, O, or * depending on what player occupies box (x, y)
    # * denotes empty
    def box_to_letter(self, x, y):
        if self.state[y][x] == -1:
            return "O"
        elif self.state[y][x] == 1:
            return "X"
        return "*"

    # Makes a move in the box (x,y) regardless of tic tac toe rules
    # x and y must each be between 0 and 2
    def autoturn_do_move_dirty(self, x, y):
        self.state[y][x] = self.currentPlayer
        self.proceed_turn(x, y)
        self.check_win()

    # Attempts to make a move in the box (x, y)
    # If the move abides by tic-tac-toe rules, then the game is updated
    # accordingly. Otherwise nothing changes.
    # Precondition: x and y must be between 0 and 2
    def autoturn_do_move(self, x, y):
        if self.is_valid(x, y):
            self.state[y][x] = self.currentPlayer
            self.proceed_turn(x, y)
            self.finished = self.check_win()

    # Makes a move in the box (x,y) regardless of tic tac toe rules
    # x and y must each be between 0 and 2. player is -1 or 1
    def do_move_dirty(self, x, y, player):
        self.state[y][x] = player
        self.proceed_turn(x, y)
        self.currentPlayer = player * -1
        self.turnsElapsed += 1
        self.lastPlayed = (x, y)
        self.finished = self.check_win()
        self.score = self.eval_mini()

    # Attempts to make a move in the box (x, y)
    # If the move abides by tic-tac-toe rules, then the game is updated
    # accordingly. Otherwise nothing changes.
    # Precondition: x and y must be between 0 and 2. player is -1 or 1
    def do_move(self, x, y, player):
        if self.is_valid(x, y):
            self.state[y][x] = player
            self.currentPlayer = player * -1
            self.turnsElapsed += 1
            self.lastPlayed = (x, y)
            self.finished = self.check_win()
            self.score = self.eval_mini()

    # Returns true if a move in box (x, y) is valid given the game's current
    # state
    def is_valid(self, x, y):
        return self.state[y][x] == 0 and self.finished == 0

    # Increments the number of turns, changes what player has the current
    # turn, and updates the last played box
    def proceed_turn(self, x, y):
        self.currentPlayer *= -1
        self.turnsElapsed += 1
        self.lastPlayed = (x, y)
        self.score = self.eval_mini()

    # Returns a list of tuples of valid moves
    def get_valid_moves(self):
        moves = []
        for y in range(3):
            for x in range(3):
                if self.is_valid(x, y):
                    moves.append((x, y))
        return moves

    # Return the column number of a winning row of the tic-tac-toe game
    # -1 if there is no winner in a column
    def check_columns(self):
        # If the sum of the numbers in a column add up to 3 or -3,
        # then X (1) or O (-1), respectively, has won
        # Col 0
        for x in range(3):
            if abs(self.state[0][x] + self.state[1][x] + self.state[2][x]) == 3:
                return x
        return -1

    # Return the row number of a winning row of the tic-tac-toe game
    # -1 if there is no winner in a row
    def check_rows(self):
        # If the sum of the numbers in a column add up to 3 or -3,
        # then X (1) or O (-1), respectively, has won
        # Col 0
        for y in range(3):
            if abs(self.state[y][0] + self.state[y][1] + self.state[y][2]) == 3:
                return y
        return -1

    # Return true if any of the diagonals of the tic-tac-toe game
    # have a 3 in a row of a single player
    def check_diagonals(self):
        if abs(self.state[0][0] + self.state[1][1] + self.state[2][2]) == 3:
            return True
        elif abs(self.state[2][0] + self.state[1][1] + self.state[0][2]) == 3:
            return True
        return False

    # Return true if all the boxes are filled and false otherwise
    # False otherwise
    def check_filled(self):
        for y in range(3):
            for x in range(3):
                if self.state[y][x] == 0:
                    return False
        return True

    # Returns the value of this board according the evaluation function:
    # 3X_2 + X_1 - 3O_2 - O_1, or +-100 for a X/O win, 0 for tie.
    def eval_mini(self):
        if self.finished == -1:
            return -100
        elif self.finished == 1:
            return 100
        elif self.finished == 10:
            return 0
        return 3*self.count_occurrences(2, 1) + self.count_occurrences(1, 1) - \
            3*self.count_occurrences(2, -1) - self.count_occurrences(1, -1)

    # Counts how many occurrences of [num_occ] of the same player are in the
    # same line while not being interrupted by the other player
    # [player] should be 1 for X, or -1 for O. [num_occ] should be 0, 1, 2, or 3
    def count_occurrences(self, num_occ, player):
        occs = 0
        opp = player * -1
        # We want the value of a line to be negative for O, and positive for X
        num_occ = num_occ * player
        # Check diagonals for [occ] in a row
        # Make sure the opponent isn't in that row
        if self.state[0][0] + self.state[1][1] + self.state[2][2] == num_occ \
            and not (self.state[0][0] == opp or self.state[1][1] == opp or
                     self.state[2][2] == opp):
            occs += 1

        if self.state[2][0] + self.state[1][1] + self.state[0][2] == num_occ \
            and not (self.state[2][0] == opp or self.state[1][1] == opp or
                     self.state[0][2] == opp):
            occs += 1
        # Check rows
        for y in range(3):
            if self.state[y][0] + self.state[y][1] + self.state[y][2] == \
                    num_occ and \
                    self.state[y][0] != opp and self.state[y][1] != opp and \
                    self.state[y][2] != opp:
                occs += 1
        # Check cols
        for x in range(3):
            if self.state[0][x] + self.state[1][x] + self.state[2][x] ==\
                    num_occ and \
                    self.state[0][x] != opp and self.state[1][x] != opp and \
                    self.state[2][x] != opp:
                occs += 1
        return occs

    # Return -1, or 1 if O or X has won the tic-tac-toe game, respectively.
    # Return 0 if the game has not been won.
    # Return 10 if the game is tied.
    def check_win(self):
        cols = self.check_columns()
        rows = self.check_rows()
        dia = self.check_diagonals()
        if cols != -1:
            return self.state[0][cols]
        elif rows != -1:
            return self.state[rows][0]
        elif dia:
            return self.state[1][1]
        elif self.check_filled():
            return 10
        return 0


