def any_tiles_row(tiles, row):
    for tile in tiles:
        if tile[1] == row:
            return True
    return False
