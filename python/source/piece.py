from turtle import pos
from tileturtle import TileTurtle
from constants import NUM_TILES_ROW, NUM_TILES_COL
from shapematrix import *


class Piece:
    clear_color = "white"
    max_col_exclusive = NUM_TILES_COL
    max_row_exclusive = NUM_TILES_ROW

    def __init__(self, screen):
        self.screen = screen
        self.tile_turtles = []
        self.tile_poses = []
        self.fillcolor = Piece.clear_color
        self.shape_matrix = []
        self.pos = (NUM_TILES_COL + 1, NUM_TILES_ROW + 1)
        pass

    def set(self, shape_matrix, fillcolor, pos):
        print("set started")
        self.shape_matrix = shape_matrix
        tile_poses = get_tile_local_poses(self.shape_matrix)
        self.pos = pos
        self.tile_poses = []
        for tile_pos in tile_poses:
            self.tile_poses.append((pos[0] + tile_pos[0], pos[1] + tile_pos[1]))
        self.fillcolor = fillcolor
        self.screen.tracer(False)
        self.tile_turtles = [
            TileTurtle(tile[0], tile[1], self.fillcolor) for tile in self.tile_poses
        ]
        self.screen.tracer(True)
        print("set ended")

    def translate(self, d_col, d_row):
        self.screen.tracer(False)
        self.pos = (self.pos[0] + d_col, self.pos[1] + d_row)
        self.tile_poses = [
            (tile[0] + d_col, tile[1] + d_row) for tile in self.tile_poses
        ]
        for i, pos in enumerate(self.tile_poses):
            self.tile_turtles[i].goto(pos[0], pos[1])
        self.screen.tracer(True)

    def rotate(self):
        rotated_shape = rotate(self.shape_matrix)
        self.shape_matrix = rotated_shape
        self.tile_poses = [
            (self.pos[0] + tile_pos[0], self.pos[1] + tile_pos[1])
            for tile_pos in get_tile_local_poses(rotated_shape)
        ]
        self.screen.tracer(False)
        for i, pos in enumerate(self.tile_poses):
            self.tile_turtles[i].goto(pos[0], pos[1])
        self.screen.tracer(True)

    def reset(self):
        print("rest started")
        self.screen.tracer(False)
        self.tile_poses = []
        self.fillcolor = Piece.clear_color
        for turtle in self.tile_turtles:
            turtle.goto(NUM_TILES_COL + 1, NUM_TILES_ROW + 1)
            turtle.color(self.fillcolor)
        self.tile_turtles = []
        self.screen.tracer(True)
        self.shape_matrix = []
        self.pos = (NUM_TILES_COL + 1, NUM_TILES_ROW + 1)
        print("rest ended")
        pass

    def get_translated_tiles(self, d_col, d_row):
        return [(tile[0] + d_col, tile[1] + d_row) for tile in self.tile_poses]

    def get_rotated_tiles(self):
        rotated_shape = rotate(self.shape_matrix)
        return [
            (self.pos[0] + tile_pos[0], self.pos[1] + tile_pos[1])
            for tile_pos in get_tile_local_poses(rotated_shape)
        ]
