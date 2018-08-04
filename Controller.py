# import UltimateBoard


def move(gui, game_state, bx, by, ix, iy):
    gui.set_valid_boards()
    game_state.do_move4(bx, by, ix, iy)
    gui.update_board(bx, by, ix, iy)
