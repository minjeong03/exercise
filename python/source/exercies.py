# Todo For the future
# 1. FIX BUGS!
#   a. rotation fails outside of board
#   b. hit unexpected code path
#   c. malfunctioning hard-drop
# 2. records input per game session
# 3. verbose log into txt file
# 4. Wow... race condition

from piece_parser import load_shape_matrices_from_file, parse_shape_matrix_from_string
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
        self.running = True

        self.setup()

        self.dec_curr_piece_row_timer = 0
        self.dec_curr_piece_row_duration_milisec = 250

        self.flush_board_timer = 0
        self.flush_board_duration_milisec = 250

        # self.shapes = []
        # self.shapes.append(parse_shape_matrix_from_string("0000\n0000\n1111\n0000"))
        self.shapes = load_shape_matrices_from_file("pieces.txt")
        self.colors = ["red", "green", "blue"]

    def stop(self):
        self.running = False

    def restart(self):
        self.screen.clearscreen()
        self.setup()

    def update(self):
        if not self.paused:
            self.update_piece()
            self.update_board()

    def flush(self):
        self.board.flush_request_top()
        self.flush_timer_on = False

    def update_board(self):
        if len(self.board.flush_requests) != 0:
            self.flush_board_timer += TICK_STEP
            if self.flush_board_timer >= self.flush_board_duration_milisec:
                self.flush()
                self.flush_board_timer -= self.flush_board_duration_milisec
        else:
            self.flush_board_timer = 0

    def update_piece(self):
        if len(self.piece.tile_poses) == 0:
            self.create_piece()
        else:
            self.dec_curr_piece_row_timer += TICK_STEP
            if self.dec_curr_piece_row_timer < self.dec_curr_piece_row_duration_milisec:
                pass
            else:
                self.dec_curr_piece_row_timer -= (
                    self.dec_curr_piece_row_duration_milisec
                )

                next_piece_tile_poses = self.piece.get_translated_tiles(0, -1)

                # Note. expects that any_tiles_occupied(curr_piece_tile_poses) returns false
                if self.board.test_any_tiles_occupied(next_piece_tile_poses):
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

    def game_over(self):
        print("game over!")
        self.restart()
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

        piece_bounding_box = get_bounding_box(self.piece.tile_poses)
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
                if not self.board.test_any_tiles_occupied(test_piece_tile_poses):
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

        if self.board.test_any_tiles_occupied(new_poses):
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
        if len(self.piece.shape_matrix) != 0:
            new_poses = self.piece.get_rotated_tiles()
            if self.are_valid_tiles_on_board(new_poses):
                self.piece.rotate()
                print("\\^0^//")

    def debug_print(self, *arg):
        if self.debug_print_enabled:
            print(arg)

    def pause(self):
        self.paused = not self.paused

    def setup(self):
        self.screen.tracer(False)
        self.screen.setup(SCREENWIDTH, SCREENHEIGHT)
        self.screen.delay(0)
        BOT_LEFT_WORLD = (
            -MARGIN_LEFT_RIGHT / PIXELS_PER_UNIT,
            -MARGIN_LEFT_RIGHT / PIXELS_PER_UNIT,
        )
        TOP_RIGHT_WORLD = (
            NUM_TILES_COL + MARGIN_LEFT_RIGHT / PIXELS_PER_UNIT,
            NUM_TILES_ROW + MARGIN_BOTTOM_TOP / PIXELS_PER_UNIT,
        )

        self.screen.setworldcoordinates(
            BOT_LEFT_WORLD[0],
            BOT_LEFT_WORLD[1],
            TOP_RIGHT_WORLD[0],
            TOP_RIGHT_WORLD[1],
        )
        self.screen.tracer(True)

        self.board = Board(NUM_TILES_COL, NUM_TILES_ROW, self.screen)
        self.piece = Piece(self.screen)

        self.screen.onclick(self.increase_row_drop_speed, 1)
        self.screen.onkeyrelease(self.pause, "Return")
        # Task. queue the inputs and procedurally handle them
        self.screen.onkeyrelease(self.drop_hard_current_piece, "space")
        self.screen.onkeyrelease(self.rotate_current_piece, "w")
        self.screen.onkeyrelease(self.move_current_piece_right, "d")
        self.screen.onkeyrelease(self.move_current_piece_left, "a")
        self.screen.onkeyrelease(self.move_current_piece_down, "s")
        self.screen.onkeyrelease(self.stop, "Escape")
        self.screen.listen()


def main():
    screen = Screen()
    tetris = Tetris(screen)

    while tetris.running:
        tetris.update()
        update()

    return "EVENTLOOP"


if __name__ == "__main__":
    msg = main()
    print(msg)
    mainloop()
