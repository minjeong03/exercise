# Bug. the current tile turtles won't clear when hard drop

from turtle import *
import math

MARGIN_BOTTOM_TOP = 30
MARGIN_LEFT_RIGHT = 30

PIXELS_PER_UNIT = 30
SHAPESIZE = PIXELS_PER_UNIT * (1 / 20)

NUM_TILES_COL = 10
NUM_TILES_ROW = 20

TICK_RATE = math.floor((1 / 60) * 1000)

SCREENWIDTH = NUM_TILES_COL * PIXELS_PER_UNIT + MARGIN_BOTTOM_TOP * 2
SCREENHEIGHT = NUM_TILES_ROW * PIXELS_PER_UNIT + MARGIN_LEFT_RIGHT * 2


class TileTurtle(Turtle):
    def __init__(self, col, row, fill_color="white"):
        Turtle.__init__(self)
        self.shape("square")
        self.resizemode("user")
        self.shapesize(SHAPESIZE, SHAPESIZE, 0.1)
        self.pensize(0.1)
        self.col = col
        self.row = row
        self.color("black", fill_color)
        self.speed(0)
        self.pu()
        self.goto(col, row)


class Tetris:
    def __init__(self, screen):
        self.debug_print_enabled = False
        self.screen = screen

        self.dec_curr_piece_row_timer = 0
        self.dec_curr_piece_row_duration_milisec = 1000

        # Q. can I pull this out as a board class?
        self.board_tiles_occupied = [
            [False for row in range(NUM_TILES_ROW)] for col in range(NUM_TILES_COL)
        ]

        self.screen.tracer(False)
        self.board_tiles = [
            [TileTurtle(col, row) for row in range(NUM_TILES_ROW)]
            for col in range(NUM_TILES_COL)
        ]
        self.screen.tracer(True)

        # Q. can I pull this out as a piece class?
        self.curr_piece_tile_turtles = []
        self.curr_piece_tile_poses = []
        self.curr_piece_fillcolor = "red"

    def update(self):
        if len(self.curr_piece_tile_poses) == 0:
            self.create_piece()
        else:
            self.dec_curr_piece_row_timer += TICK_RATE
            if self.dec_curr_piece_row_timer < self.dec_curr_piece_row_duration_milisec:
                pass
            else:
                self.dec_curr_piece_row_timer -= (
                    self.dec_curr_piece_row_duration_milisec
                )

                next_piece_tile_poses = [
                    (tile_pos[0], tile_pos[1] - 1)
                    for tile_pos in self.curr_piece_tile_poses
                ]

                # Note. expects that any_tiles_occupied(curr_piece_tile_poses) returns false
                if self.any_tiles_occupied(
                    next_piece_tile_poses, self.board_tiles_occupied
                ):
                    if self.any_tiles_row(self.curr_piece_tile_poses, NUM_TILES_ROW):
                        self.game_over()
                    else:
                        self.settle_tiles_on_board_clear_current_tiles(
                            self.curr_piece_tile_poses
                        )
                elif self.any_tiles_row(self.curr_piece_tile_poses, 0):
                    self.settle_tiles_on_board_clear_current_tiles(
                        self.curr_piece_tile_poses
                    )
                else:
                    self.curr_piece_tile_poses = next_piece_tile_poses
                    self.screen.tracer(False)
                    for i, tile_pos in enumerate(self.curr_piece_tile_poses):
                        self.curr_piece_tile_turtles[i].goto(tile_pos[0], tile_pos[1])
                    self.screen.tracer(True)

        self.screen.ontimer(self.update, TICK_RATE)

    def game_over(self):
        print("game over!")
        pass

    # Refactor. this function does too much jobs
    # what it does right now:
    # 1. set tiles on the board
    # 2. clear current piece
    def settle_tiles_on_board_clear_current_tiles(self, tile_poses):
        self.screen.tracer(False)
        for tile_pos in tile_poses:
            self.board_tiles_occupied[tile_pos[0]][tile_pos[1]] = True
            self.board_tiles[tile_pos[0]][tile_pos[1]].fillcolor(
                self.curr_piece_fillcolor
            )

        # Bug. don't clear tiles as white when hard-drop piece
        self.curr_piece_tile_turtles = []
        self.curr_piece_tile_poses = []
        self.screen.tracer(True)

    def create_piece(self):
        if len(self.curr_piece_tile_poses) != 0:
            print(
                "WHAT THE HECK? -- transfer the current piece prior to creating new piece!"
            )
            return

        self.curr_piece_tile_poses = [
            (4, NUM_TILES_ROW),
            (5, NUM_TILES_ROW),
            (6, NUM_TILES_ROW),
        ]
        self.screen.tracer(False)
        self.curr_piece_tile_turtles = [
            TileTurtle(tile[0], tile[1], self.curr_piece_fillcolor)
            for tile in self.curr_piece_tile_poses
        ]
        self.screen.tracer(True)

    def any_tiles_row(self, tiles, row):
        for tile in tiles:
            if tile[1] == row:
                return True
        return False

    def are_valid(self, tiles):
        for tile in tiles:
            if not self.is_valid(tile):
                return False
        return True

    def is_valid(self, tile):
        if (
            tile[0] < 0
            or tile[0] >= NUM_TILES_COL
            or tile[1] < 0
            or tile[1] >= NUM_TILES_ROW
        ):
            return False
        return True

    # tiles = list of tuples (col, row)
    # board_tiles_occupied = 2D list [col][row]
    # Note: this function checks valid tiles and ingores invalid tiles
    def any_tiles_occupied(self, tiles, board_tiles_occupied):
        for tile in tiles:
            if self.is_valid(tile) and board_tiles_occupied[tile[0]][tile[1]] == True:
                return True
        return False

    def increase_row_drop_speed(self, x, y):
        self.dec_curr_piece_row_duration_milisec -= 50

    def drop_hard_current_piece(self):
        print("HI")
        # bounding box (bot_left, top_right) = (min_col, min_row) (max_col, max_row)
        min_col = NUM_TILES_COL
        max_col = -1
        min_row = NUM_TILES_ROW
        max_row = -1

        for tile_pos in self.curr_piece_tile_poses:
            row = tile_pos[1]
            col = tile_pos[0]
            if min_col > col:
                min_col = col
            elif max_col < col:
                max_col = col
            if min_row > row:
                min_row = row
            elif max_row < row:
                max_row = row

        self.debug_print([(min_col, max_col), (min_row, max_row)])

        # highest row in the board where col ranges from (left, right)
        k_last_max_row = NUM_TILES_ROW - 1
        highest_row = -1
        for col in range(min_col, max_col + 1):
            for row, value in enumerate(reversed(self.board_tiles_occupied[col])):
                if value == True:
                    highest_row = k_last_max_row - row
                    self.debug_print(("found one ", row, highest_row))
                    break  # becase iterating descending order

        # the piece might go as deep as bounding box height(max_row - min_row + 1) - 1 from(subtracted from) highest,
        # which means, the possible minimum row ranges (highest - (max_row-min_row+1) + 1, highest + 1)
        self.debug_print(self.curr_piece_tile_poses)
        top_row = highest_row + 1
        deepest_row = max(highest_row - (max_row - min_row), 0)

        self.debug_print((deepest_row, top_row))
        for possible_row in range(deepest_row, top_row + 1):
            test_piece_tile_poses = [
                (tile_pos[0], possible_row) for tile_pos in self.curr_piece_tile_poses
            ]
            self.debug_print(test_piece_tile_poses)
            if self.are_valid(test_piece_tile_poses):
                if not self.any_tiles_occupied(
                    test_piece_tile_poses, self.board_tiles_occupied
                ):
                    self.settle_tiles_on_board_clear_current_tiles(
                        test_piece_tile_poses
                    )
                    print("\\^0^/")
                    return
            else:
                self.game_over()
                return
        print("hit unexpected code path")

    def print_board(self):
        for col in self.board_tiles_occupied:
            print(col)

    def rotate_current_piece(self):
        pass

    def move_current_piece_right(self):
        pass

    def move_current_piece_left(self):
        pass

    def debug_print(self, *arg, **kwrds):
        if self.debug_print_enabled:
            print(arg, kwrds)


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

    screen.onkeyrelease(tetris.drop_hard_current_piece, "space")
    screen.onkeyrelease(tetris.rotate_current_piece, "uparrow")
    screen.onkeyrelease(tetris.move_current_piece_right, "rightarrow")
    screen.onkeyrelease(tetris.move_current_piece_left, "leftarrow")
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
