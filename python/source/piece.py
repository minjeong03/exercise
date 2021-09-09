from tileturtle import TileTurtle
from constants import NUM_TILES_ROW, NUM_TILES_COL


class Piece:
    clear_color = "white"
    max_col_exclusive = NUM_TILES_COL
    max_row_exclusive = NUM_TILES_ROW

    def __init__(self, screen):
        self.screen = screen
        self.tile_turtles = []
        self.tile_poses = []
        self.fillcolor = Piece.clear_color
        pass

    def set(self, tile_poses, fillcolor):
        self.tile_poses = tile_poses
        self.fillcolor = fillcolor
        self.screen.tracer(False)
        self.tile_turtles = [
            TileTurtle(tile[0], tile[1], self.fillcolor) for tile in self.tile_poses
        ]
        self.screen.tracer(True)
        pass

    def translate_to(self, new_poses):
        self.screen.tracer(False)
        self.tile_poses = new_poses
        for i, pos in enumerate(self.tile_poses):
            self.tile_turtles[i].goto(pos[0], pos[1])
        self.screen.tracer(True)

    def reset(self):
        self.screen.tracer(False)
        self.tile_poses = []
        self.fillcolor = Piece.clear_color
        for turtle in self.tile_turtles:
            turtle.goto(NUM_TILES_COL + 1, NUM_TILES_ROW + 1)
            turtle.color(self.fillcolor)
        self.tile_turtles = []
        self.screen.tracer(True)
        pass

    # returns [(min_col, min_row), (max_col, max_row)]
    def get_bounding_box(self):
        min_col = Piece.max_col_exclusive
        min_row = Piece.max_row_exclusive
        max_col = 0
        max_row = 0
        for tile_pos in self.tile_poses:
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
        return [(min_col, min_row), (max_col, max_row)]

    def get_translated_tiles(self, d_col, d_row):
        return [(tile[0] + d_col, tile[1] + d_row) for tile in self.tile_poses]

    def get_rotated_tiles(self):
        pass


class PieceOld:
    def __init__(self):
        self.mat = []

    def rotate(self):
        result = self.mat[:]
        self.mat = rotate_sqaure(result)
        self.update_tiles()

    def set_from_string(self, str):
        result = []
        current = []
        for char in str:
            if char == "\n":
                result.append(current)
                current = []
            elif char == "0":
                current.append(0)
            elif char == "1":
                current.append(1)
        self.mat = result
        self.update_tiles()

    def update_tiles(self):
        self.tiles = []
        for y, row in enumerate(self.mat):
            curr_y = -y - 1
            for x, col in enumerate(self.mat[curr_y]):
                if col == 1:
                    pass  # self.tiles.append(Tile((self.pos[0] + x, self.pos[1] + y)))


"""
rotate 2D list 90 degree clockwise
e.g)
    [[1, 2],      [[3, 1],        [[4, 3],
    [3, 4]]  =>   [4, 2]]    =>   [2, 1]]    =>
impl)
     transpose and then do the symmetry about y axis
"""


def rotate_sqaure(mat):
    if len(mat) <= 0:
        return
    transposed = [[row[i] for row in mat] for i, e in enumerate(mat[0])]
    # print(transposed)
    y_symmetric = [[row[-1 - i] for i, col in enumerate(row)] for row in transposed]
    # print(y_symmetric)
    return y_symmetric
