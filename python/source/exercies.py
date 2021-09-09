# Todo For the future
# 1. FIX BUGS!
#   a. rotation fails outside of board
#   b. hit unexpected code path
#   c. malfunctioning hard-drop
# 2. records input per game session
# 3. verbose log into txt file

from piece_parser import load_shape_matrices_from_file
from turtle import *
from constants import *
from piece import Piece
from board import Board
from tile_utility import *
from random import randint
from copy import copy


class Tetris:
    def __init__(self, screen):
        self.paused = False
        self.debug_print_enabled = False
        self.screen = screen

        self.dec_curr_piece_row_timer = 0
        self.dec_curr_piece_row_duration_milisec = 500

        self.board = Board(NUM_TILES_COL, NUM_TILES_ROW, self.screen)
        self.piece = Piece(self.screen)

        self.shapes = load_shape_matrices_from_file("pieces.txt")
        self.colors = ["red", "green", "blue"]

    def restart(self):
        pass

    def update(self):
        if not self.paused:
            if len(self.piece.tile_poses) == 0:
                self.create_piece()
            else:
                self.dec_curr_piece_row_timer += TICK_RATE if TICK_ENABLED else 0
                if (
                    self.dec_curr_piece_row_timer
                    < self.dec_curr_piece_row_duration_milisec
                ):
                    pass
                else:
                    self.dec_curr_piece_row_timer -= (
                        self.dec_curr_piece_row_duration_milisec
                    )

                    next_piece_tile_poses = self.piece.get_translated_tiles(0, -1)

                    # Note. expects that any_tiles_occupied(curr_piece_tile_poses) returns false
                    if self.board.any_tiles_occupied(next_piece_tile_poses):
                        if any_tiles_row(self.piece.tile_poses, self.board.num_row):
                            self.game_over()
                        else:
                            self.board.set_tiles_occupied(
                                self.piece.tile_poses, self.piece.fillcolor
                            )
                            self.piece.reset()
                    elif any_tiles_row(self.piece.tile_poses, 0):
                        self.board.set_tiles_occupied(
                            self.piece.tile_poses, self.piece.fillcolor
                        )
                        self.piece.reset()
                    else:
                        self.piece.translate(0, -1)
        self.screen.ontimer(self.update, TICK_RATE)

    def game_over(self):
        print("game over!")
        pass

    def create_piece(self):
        if len(self.piece.tile_poses) != 0:
            print(
                "WHAT THE HECK? -- transfer the current piece prior to creating new piece!"
            )
            return

        piece_shape = copy(self.shapes[randint(0, len(self.shapes) - 1)])
        piece_color = copy(self.colors[randint(0, len(self.colors) - 1)])
        self.piece.set(
            piece_shape, piece_color, (self.board.num_col // 2, self.board.num_row)
        )

    def increase_row_drop_speed(self, x, y):
        self.dec_curr_piece_row_duration_milisec -= 50

    def drop_hard_current_piece(self):
        print("drop_hard")

        piece_bounding_box = self.piece.get_bounding_box()
        self.debug_print(("bb: ", piece_bounding_box))

        # highest row in the board where col ranges from (left, right)
        highest_row = self.board.get_highest_tile_occupied(
            piece_bounding_box[0][0], piece_bounding_box[1][0] + 1
        )

        # the piece might go as deep as bounding box height(max_row - min_row + 1) - 1 from(subtracted from) highest,
        # which means, the possible minimum row ranges (highest - (max_row-min_row+1) + 1, highest + 1)
        self.debug_print(("curr: ", self.piece.tile_poses))
        top_row = highest_row + 1
        deepest_row = max(
            highest_row - (piece_bounding_box[1][1] - piece_bounding_box[0][1]), 0
        )
        self.debug_print(("(bottom, top): ", (deepest_row, top_row)))
        for possible_row in range(deepest_row, top_row + 1):
            d_row = piece_bounding_box[0][1] - (possible_row)
            test_piece_tile_poses = [
                (tile_pos[0], tile_pos[1] - d_row) for tile_pos in self.piece.tile_poses
            ]
            self.debug_print(("test poses = ", test_piece_tile_poses))
            if self.board.are_valid(test_piece_tile_poses):
                if not self.board.any_tiles_occupied(test_piece_tile_poses):
                    self.board.set_tiles_occupied(
                        test_piece_tile_poses, self.piece.fillcolor
                    )
                    self.piece.reset()
                    print("\\^0^/")
                    return
            else:
                self.game_over()
                return
        print("hit unexpected code path")

    def are_valid_tiles_on_board(self, new_poses):
        for tile in new_poses:
            if not self.board.is_valid_soft(tile):
                self.debug_print("hit the wall")
                return False

        if self.board.any_tiles_occupied(new_poses):
            self.debug_print("hit the occupied tile")
            return False

        return True

    def move_current_piece(self, d_col, d_row):
        new_poses = self.piece.get_translated_tiles(d_col, d_row)

        if self.are_valid_tiles_on_board(new_poses):
            self.piece.translate(d_col, d_row)

    def move_current_piece_right(self):
        print("right")
        self.move_current_piece(+1, 0)

    def move_current_piece_left(self):
        print("left")
        self.move_current_piece(-1, 0)

    def move_current_piece_down(self):
        print("down")
        self.move_current_piece(0, -1)

    def rotate_current_piece(self):
        print("rotate")
        new_poses = self.piece.get_rotated_tiles()
        if self.are_valid_tiles_on_board(new_poses):
            self.piece.rotate()
            print("\\^0^//")

    def debug_print(self, *arg):
        if self.debug_print_enabled:
            print(arg)

    def pause(self):
        self.paused = not self.paused


def tick():
    pass


def setup():
    screen = Screen()
    screen.setup(SCREENWIDTH, SCREENHEIGHT)
    screen.delay(0)
    BOT_LEFT_WORLD = (
        -MARGIN_LEFT_RIGHT / PIXELS_PER_UNIT,
        -MARGIN_LEFT_RIGHT / PIXELS_PER_UNIT,
    )
    TOP_RIGHT_WORLD = (
        NUM_TILES_COL + MARGIN_LEFT_RIGHT / PIXELS_PER_UNIT,
        NUM_TILES_ROW + MARGIN_BOTTOM_TOP / PIXELS_PER_UNIT,
    )

    screen.setworldcoordinates(
        BOT_LEFT_WORLD[0],
        BOT_LEFT_WORLD[1],
        TOP_RIGHT_WORLD[0],
        TOP_RIGHT_WORLD[1],
    )
    tetris = Tetris(screen)
    screen.ontimer(tetris.update, TICK_RATE)
    screen.onclick(tetris.increase_row_drop_speed, 1)

    screen.onkeyrelease(tetris.pause, "Escape")
    screen.onkeyrelease(tetris.drop_hard_current_piece, "space")
    screen.onkeyrelease(tetris.rotate_current_piece, "w")
    screen.onkeyrelease(tetris.move_current_piece_right, "d")
    screen.onkeyrelease(tetris.move_current_piece_left, "a")
    screen.onkeyrelease(tetris.move_current_piece_down, "s")
    screen.listen()


def main():
    tracer(False)
    setup()
    tracer(True)

    return "EVENTLOOP"


if __name__ == "__main__":
    msg = main()
    print(msg)
    mainloop()
