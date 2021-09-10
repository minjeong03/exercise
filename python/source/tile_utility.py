# tiles(col, row)
def any_tiles_row(tiles, row):
    for tile in tiles:
        if tile[1] == row:
            return True
    return False


# returns [(min_col, min_row), (max_col, max_row)]
def get_bounding_box(tiles):
    min_col = 100
    min_row = 100
    max_col = 0
    max_row = 0
    for tile_pos in tiles:
        row = tile_pos[1]
        col = tile_pos[0]
        if min_col > col:
            min_col = col
        if max_col < col:
            max_col = col
        if min_row > row:
            min_row = row
        if max_row < row:
            max_row = row
    return [(min_col, min_row), (max_col, max_row)]
