from tileturtle import TileTurtle


class Board:
    def __init__(self, num_col, num_row, screen):
        self.screen = screen
        self.num_row = num_row
        self.num_col = num_col
        self.occupied_tiles = [
            [False for row in range(self.num_row)] for col in range(self.num_col)
        ]

        self.screen.tracer(False)
        self.tile_turtles = [
            [TileTurtle(col, row) for row in range(self.num_row)]
            for col in range(self.num_col)
        ]
        self.screen.tracer(True)
        pass

    # tiles = list of tuples (col, row)
    # Note: this function checks valid tiles and ingores invalid tiles
    def any_tiles_occupied(self, tiles):
        for tile in tiles:
            if self.is_valid(tile) and self.occupied_tiles[tile[0]][tile[1]] == True:
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

    def set_tiles_occupied(self, tile_poses, fillcolor):
        self.screen.tracer(False)
        for tile_pos in tile_poses:
            self.occupied_tiles[tile_pos[0]][tile_pos[1]] = True
            self.tile_turtles[tile_pos[0]][tile_pos[1]].fillcolor(fillcolor)
        self.screen.tracer(True)

    def get_highest_tile_occupied(self, start_col, end_col):
        k_last_max_row = self.num_row - 1
        highest_row = -1
        for col in range(start_col, end_col):
            for row, value in enumerate(reversed(self.occupied_tiles[col])):
                if value == True:
                    real_row = k_last_max_row - row
                    if highest_row < real_row:
                        highest_row = real_row
                    break  # becase iterating descending order
        return highest_row

    def print(self):
        pass
