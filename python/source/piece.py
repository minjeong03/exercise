from render import draw_square
from constants import *
import sys
import os

k_piece_ended_format_code = "\n\n"


def load_pieces_from_file(file_name):
    pieces = []
    with open(os.path.join(sys.path[0], "..\data", file_name), "r") as f:
        content = f.read()
        start_pos = 0
        while content.find(k_piece_ended_format_code, start_pos) != -1:
            last_pos = content.find(k_piece_ended_format_code, start_pos)
            start_pos = last_pos + len(k_piece_ended_format_code)
            piece_str = content[start_pos : last_pos + 1]
            piece = Piece()
            piece.set_from_string(piece_str)
            pieces.append(piece)
    return pieces


class Tile:
    def __init__(self, relative_pos_to_piece):
        self.fill_color = k_default_tile_fill_color
        self.outline_color = k_default_tile_outline_color
        self.size_in_unit = 1
        self.inner_size_ratio = 0.9
        self.fill_size = self.size_in_unit * self.inner_size_ratio
        self.relative_pos_to_piece = relative_pos_to_piece

    def render(self, left_bottom_point):
        left_bottom_point = (
            left_bottom_point[0] + self.relative_pos_to_piece[0],
            left_bottom_point[1] + self.relative_pos_to_piece[1],
        )
        print(left_bottom_point)
        draw_square(left_bottom_point, to_pixels(self.size_in_unit), self.fill_color)
        outline_pixels = (to_pixels(self.size_in_unit) - to_pixels(self.fill_size)) / 2
        outline_left_bottom_point = (
            left_bottom_point[0] + outline_pixels,
            left_bottom_point[1] + outline_pixels,
        )
        draw_square(
            outline_left_bottom_point, to_pixels(self.fill_size), self.outline_color
        )


class Piece:
    def __init__(self):
        self.mat = []
        self.pos = (0, 0)
        self.tiles = []

    def render(self):
        for tile in self.tiles:
            tile.render(self.pos)

    def rotate(self):
        result = self.mat[:]
        self.mat = rotate_sqaure(result)

    def set_from_string(self, str):
        result = []
        current = []
        for letter in str:
            if letter == "\n":
                result.append(current)
                current = []
            elif letter == "0":
                current.append(0)
            elif letter == "1":
                current.append(1)
        self.mat = result
        self.tiles = []
        for x, row in enumerate(self.mat):
            curr_x = -x - 1
            for y, col in enumerate(self.mat[curr_x]):
                if col == 1:
                    self.tiles.append(Tile((x, y)))


# rotate 2D list 90 degree clockwise
# e.g)
# [[1, 2],      [[3, 1],        [[4, 3],
#  [3, 4]]  =>   [4, 2]]    =>   [2, 1]]    =>
# impl: transpose and then do the symmetry about y axis
def rotate_sqaure(mat):
    if len(mat) <= 0:
        return
    transposed = [[row[i] for row in mat] for i, e in enumerate(mat[0])]
    # print(transposed)
    y_symmetric = [[row[-1 - i] for i, col in enumerate(row)] for row in transposed]
    # print(y_symmetric)
    return y_symmetric


if __name__ == "__main__":
    piece = Piece()
    tile = Tile((0, 0))
    piece.set_from_string("0000\n0000\n1111\n0000")