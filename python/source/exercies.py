# CREATE PIECE....................................
# what's the problem..........?
# I want to have new piece created out of boundary, but I only have the board-size number of tile turtles
# Who'drawing the new piece? and when any tile of new piece enters boundary, how to change the drawing turtle
# to the board's turtle?
# Okay, let's figure that out first
# okay... there's going to be tile turtles for the new piece and
# once the piece is settled down, the ownership for drawing tiles for the piece is transfered to the board

# What is the condition I should create new piece?
# when curr piece is empty.

# HOW TO TICK()!?@!@!@!@!@!

# QUEUE INPUTS??? or JUST APPLY ??????

# SO BUGGY!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Bug. how to check game_over() when the tiles are only testable within the board?
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
        self.screen = screen

        self.dec_curr_piece_row_timer = 0
        self.dec_curr_piece_row_duration_milisec = 1000

        # Q. can I pull this out as a board class?
        self.board_tiles_occupied = [
            [False for row in range(NUM_TILES_ROW)] for col in range(NUM_TILES_COL)
        ]
        # print(self.board_tiles_occupied)

        self.screen.tracer(False)
        self.board_tiles = [
            [TileTurtle(col, row) for row in range(NUM_TILES_ROW)]
            for col in range(NUM_TILES_COL)
        ]
        # print(self.board_tiles)
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

                # collision check against board
                if self.check_collision(
                    next_piece_tile_poses, self.board_tiles_occupied
                ):
                    self.settle_tiles_on_board_clear_current_tiles(
                        self.curr_piece_tile_poses
                    )

                else:
                    # if no collision
                    self.screen.tracer(False)
                    self.curr_piece_tile_poses = next_piece_tile_poses
                    for i, tile_pos in enumerate(self.curr_piece_tile_poses):
                        self.curr_piece_tile_turtles[i].goto(tile_pos[0], tile_pos[1])
                    self.screen.tracer(True)

        self.screen.ontimer(self.update, TICK_RATE)

    def settle_tiles_on_board_clear_current_tiles(self, tile_poses):
        self.screen.tracer(False)
        self.curr_piece_tile_turtles = []
        for tile_pos in tile_poses:
            self.board_tiles_occupied[tile_pos[0]][tile_pos[1]] = True
            self.board_tiles[tile_pos[0]][tile_pos[1]].fillcolor(
                self.curr_piece_fillcolor
            )
        for col in self.board_tiles_occupied:
            print(col)
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

    def is_out_of_board(self, tile):
        if tile[0] < 0 or tile[0] >= NUM_TILES_COL or tile[1] < 0:
            return True
        return False

    def check_collision(self, next_piece_tile_poses, board_tiles_occupied):
        for moving_tile in next_piece_tile_poses:
            # this piece just has been created outside of board
            if moving_tile[1] >= NUM_TILES_ROW:
                return False
            if self.is_out_of_board(moving_tile):
                return True
            if board_tiles_occupied[moving_tile[0]][moving_tile[1]] == True:
                return True
        return False

    def increase_row_drop_speed(self, x, y):
        self.dec_curr_piece_row_duration_milisec -= 50

    def drop_hard_current_piece_2(self):
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

        print([(min_col, max_col), (min_row, max_row)])

        # highest row in the board where col ranges from (left, right)
        k_last_max_row = len(self.board_tiles_occupied[0]) - 1
        highest_row = 0
        for col in range(min_col, max_col + 1):
            for row, value in enumerate(reversed(self.board_tiles_occupied[col])):
                if value == True:
                    real_row = k_last_max_row - row
                    if highest_row < real_row:
                        highest_row = real_row
                    break  # becase iterating descending order
        print("highest row = %d" % highest_row)
        print((min_row - highest_row, max_row - highest_row + 1))
        print(self.curr_piece_tile_poses)
        for d_row in reversed(
            range(min_row - highest_row - 1, max_row - highest_row + 1)
        ):
            print(d_row)
            test_piece_tile_poses = [
                (tile_pos[0], tile_pos[1] - d_row)
                for tile_pos in self.curr_piece_tile_poses
            ]
            print(test_piece_tile_poses)
            if (
                self.check_collision(test_piece_tile_poses, self.board_tiles_occupied)
                == False
            ):
                self.settle_tiles_on_board_clear_current_tiles(test_piece_tile_poses)
                print("\\^0^/")
                return

    def drop_hard_current_piece_1(self):

        min_col = NUM_TILES_COL
        max_col = -1
        min_row = NUM_TILES_ROW
        col_at_lowest = min_col

        # Q. what if create a Piece class that has methods querying such things? !!!!
        # find the col of the tile where the tile is the lowest row among all the tiles of the piece
        # what if the col at lowest row doesn't collide but the col at next lowest collide?
        # should sort the cols by rows?
        for tile_pos in self.curr_piece_tile_poses:
            row = tile_pos[1]
            col = tile_pos[0]
            if min_col > col:
                min_col = col
            elif max_col < col:
                max_col = col
            if min_row > row:
                min_row = row
                col_at_lowest = col

        # find the highest row True where col ranges from min_col to max_col
        last_max_row = len(self.board_tiles_occupied[0]) - 1
        col_at_max_row = 0
        max_row = 0
        for col in range(min_col, max_col + 1):
            for row, value in enumerate(reversed(self.board_tiles_occupied[col])):
                if value == True:
                    real_row = last_max_row - row
                    if max_row < real_row:
                        max_row = real_row
                        col_at_max_row = col
                    break  # becase iterating descending order

        # DOES IT gaurantee that other tiles of current piece don't collide with board?
        # SHOULD I JUST CHECK FOR ALL TILES?
        max_row + 1

    def rotate_current_piece(self):
        pass

    def move_current_piece_right(self):
        pass

    def move_current_piece_left(self):
        pass


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

    screen.onkeyrelease(tetris.drop_hard_current_piece_1, "space")
    screen.onkeyrelease(tetris.drop_hard_current_piece_2, "Return")
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
