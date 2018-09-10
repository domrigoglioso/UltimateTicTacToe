from UltimateTicTacToeGUI import UltimateBoardFrame
from UltimateBoard import GameTree


def run(gui: UltimateBoardFrame):
    gui.root.mainloop()


def move(gui: UltimateBoardFrame, bx, by, ix, iy):
    gui.set_valid_boards()
    gui.ub.do_move4(bx, by, ix, iy)
    gui.update_board(bx, by, ix, iy)
    # gui.root.mainloop()


def random_move(gui):
    gui.set_valid_boards()
    gui.ub.random_move()
    lastMove = gui.ub.lastMove
    gui.update_board(lastMove[0], lastMove[1], lastMove[2], lastMove[3])
    # gui.root.mainloop()


def minimax_move(gui):
    if gui.ub.finished:
        return
    gui.set_valid_boards()
    next_move = GameTree.minimax_tree_move(gui.ub, 4, gui.ub.currentPlayer)
    gui.update_board(next_move[0], next_move[1], next_move[2], next_move[3])
