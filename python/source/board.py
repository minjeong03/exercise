from turtle import Turtle
from tile_utility import get_bounding_box
from tileturtle import TileTurtle


class Board:
    flush_ready_color = "grey"

    def __init__(self, num_col, num_row, screen):
        self.screen = screen
        self.num_row = num_row
        self.num_col = num_col

        # Note. indexing is reversed for board. turtles[row][col] & occupied_tiles[row][col]
        self.occupied_tiles = [
            [False for col in range(self.num_col)] for row in range(self.num_row)
        ]
        # Perf. later ...
        # self.row_dirty = [False for row in range(self.num_row)]

        # consider State Machine for visual states?
        # flush animation visual states:
        #  on_start_flushing = grey
        #  flushing = some animation
        # Q. what should I call the moment of getting flushing visual state ended?
        self.flush_requests = []

        self.screen.tracer(False)
        self.tile_turtles = [
            [TileTurtle(col, row) for col in range(self.num_col)]
            for row in range(self.num_row)
        ]
        self.screen.tracer(True)
        pass

    # tiles = list of tuples (col, row)
    # Note: this function checks valid tiles and ingores invalid tiles
    def test_any_tiles_occupied(self, tiles):
        for tile in tiles:
            if self.is_valid(tile) and self.occupied_tiles[tile[1]][tile[0]] == True:
                return True
        return False

    def are_valid(self, tiles):
        for tile in tiles:
            if not self.is_valid(tile):
                return False
        return True

    def is_valid_soft(self, tile):
        if tile[0] < 0 or tile[0] >= self.num_col or tile[1] < 0:
            return False
        return True

    def is_valid(self, tile):
        if (
            tile[0] < 0
            or tile[0] >= self.num_col
            or tile[1] < 0
            or tile[1] >= self.num_row
        ):
            return False
        return True

    def set_row_fillcolor(self, row, fillcolor):
        self.screen.tracer(False)
        for turtle in self.tile_turtles[row]:
            turtle.fillcolor(fillcolor)
        self.screen.tracer(False)

    def all_occupied_row(self, row):
        for tile in self.occupied_tiles[row]:
            if tile == False:
                return False
        return True

    def flush_request_top(self):
        if len(self.flush_requests) != 0:
            self.screen.tracer(False)
            rows_to_flush = self.flush_requests.pop(0)  # Perf. queue?
            for start_row in reversed(rows_to_flush):
                end_row = self.num_row - 1
                for row in range(start_row, end_row):
                    for col, turtle in enumerate(self.tile_turtles[row]):
                        if self.occupied_tiles[row + 1][col]:
                            turtle.fillcolor(
                                self.tile_turtles[row + 1][col].fillcolor()
                            )
                        else:
                            turtle.fillcolor("white")
                        self.occupied_tiles[row][col] = self.occupied_tiles[row + 1][
                            col
                        ]
                end_row = end_row - 1
            for turtle in self.tile_turtles[self.num_row - 1]:
                turtle.fillcolor("white")
            self.screen.tracer(True)

    def set_tiles_occupied(self, tile_poses, fillcolor):
        self.screen.tracer(False)
        for tile_pos in tile_poses:
            self.occupied_tiles[tile_pos[1]][tile_pos[0]] = True
            self.tile_turtles[tile_pos[1]][tile_pos[0]].fillcolor(fillcolor)

        bb = get_bounding_box(tile_poses)
        rows_to_flush = []
        for row in range(bb[0][1], bb[1][1] + 1):
            if self.all_occupied_row(row):
                rows_to_flush.append(row)

        if len(rows_to_flush) != 0:
            self.flush_requests.append(rows_to_flush)
            for row in rows_to_flush:
                self.set_row_fillcolor(row, Board.flush_ready_color)
        self.screen.tracer(True)

    def get_highest_tile_occupied(self, start_col, end_col):
        k_last_max_row = self.num_row - 1
        highest_row = -1
        for reversed_row, row in enumerate(reversed(self.occupied_tiles)):
            for col in range(start_col, end_col):
                if row[col] == True:
                    real_row = k_last_max_row - reversed_row
                    if highest_row < real_row:
                        highest_row = real_row
                    break  # becase iterating descending order
        return highest_row

    def print(self):
        for row in self.occupied_tiles:
            print(row)
