from render import *
from board import Board
from piece import Piece, Tile, load_pieces_from_file

g_board = Board()
g_pieces = load_pieces_from_file("pieces.txt")


def on_left(x, y):
    pass


def on_middle(x, y):
    pass


def on_right(x, y):
    pass


if __name__ == "__main__":
    main_init(on_left, on_middle, on_right)
    g_board.render()
    if len(g_pieces) != 0:
        g_pieces[0].render()
        print(g_pieces[0])
    mainloop()
