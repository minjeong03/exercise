from render import *
from board import Board
from piece import Piece, Tile, load_pieces_from_file

g_board = Board()
g_pieces = load_pieces_from_file("pieces.txt")


def on_left(x, y):
    clear()
    g_board.render()
    g_pieces[0].rotate()
    g_pieces[0].render()


def on_middle(x, y):
    print("on_middle")


def on_right(x, y):
    pass


def run_my_func(func, *args):
    func(*args)


if __name__ == "__main__":
    run_my_func(on_middle, 0, 0)

    main_init(on_left, on_middle, on_right)
    g_board.render()
    if len(g_pieces) != 0:
        g_pieces[0].render()
    mainloop()
