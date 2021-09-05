from render import draw_line
from constants import *


class Board:
    def __init__(self):
        self.size = k_default_board_size

    def render(self):
        for col in range(self.size[1] + 1):
            y_in_pixels = to_pixels(col)
            p0x_in_pixels = to_pixels(0)
            p1x_in_pixels = to_pixels(self.size[0])
            p0 = (p0x_in_pixels, y_in_pixels)
            p1 = (p1x_in_pixels, y_in_pixels)
            draw_line(p0, p1, 1, (0, 0, 0))

        for row in range(self.size[0] + 1):
            x_in_pixels = to_pixels(row)
            p0y_in_pixels = to_pixels(0)
            p1y_in_pixels = to_pixels(self.size[1])
            p0 = (x_in_pixels, p0y_in_pixels)
            p1 = (x_in_pixels, p1y_in_pixels)
            draw_line(p0, p1, 1, (0, 0, 0))


if __name__ == "__main__":
    board = Board()
    board.render()
