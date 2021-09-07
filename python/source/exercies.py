from turtle import *

MARGIN_BOTTOM_TOP = 30
MARGIN_LEFT_RIGHT = 30

PIXELS_PER_UNIT = 30
SHAPESIZE = PIXELS_PER_UNIT * (1 / 20)

NUM_TILES_COL = 10
NUM_TILES_ROW = 20

SCREENWIDTH = NUM_TILES_COL * PIXELS_PER_UNIT + MARGIN_BOTTOM_TOP * 2
SCREENHEIGHT = NUM_TILES_ROW * PIXELS_PER_UNIT + MARGIN_LEFT_RIGHT * 2


class TileTurtle(Turtle):
    def __init__(self, col, row):
        Turtle.__init__(self)
        self.shape("square")
        self.resizemode("user")
        self.shapesize(SHAPESIZE, SHAPESIZE, 0.1)
        self.pensize(0.1)
        self.col = col
        self.row = row
        self.color("black", "white")
        self.speed(0)
        self.pu()
        self.goto(col, row)


class Tetris:
    def __init__(self, screen):
        self.screen = screen
        self.screen.tracer(False)
        self.tiles = [
            [TileTurtle(col, row) for col in range(NUM_TILES_COL)]
            for row in range(NUM_TILES_ROW)
        ]
        self.currTiles = []
        self.screen.tracer(True)

    def update(self):
        self.screen.tracer(False)
        nextTiles = [(tile[0] - 1, tile[1]) for tile in self.currTiles]
        for tile in self.currTiles:
            self.tiles[tile[0]][tile[1]].fillcolor("white")
        for tile in nextTiles:
            self.tiles[tile[0]][tile[1]].fillcolor("red")
        self.screen.tracer(True)
        self.currTiles = nextTiles


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


def main():
    tracer(False)
    setup()
    tracer(True)
    tick()
    return "EVENTLOOP"


if __name__ == "__main__":
    msg = main()
    print(msg)
    mainloop()
