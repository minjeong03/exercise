# shape matrix coordinate
# is upside down (vs world coordinate)


def rotate(mat):
    if len(mat) <= 0:
        return
    transposed = [[row[i] for row in mat] for i, e in enumerate(mat[0])]
    # print(transposed)
    y_symmetric = [[row[-1 - i] for i, col in enumerate(row)] for row in transposed]
    # print(y_symmetric)
    return y_symmetric


def get_tile_local_poses(mat):
    tile_poses = []
    num_row = len(mat)
    half_num_col = len(mat[0]) // 2
    for row, row_val in enumerate(mat):
        world_row = num_row - row - 1
        for col, col_val in enumerate(row_val):
            if col_val == True:
                tile_poses.append((col - half_num_col, world_row))
    return tile_poses


if __name__ == "__main__":
    shape_matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]
    print(shape_matrix)
    print(get_tile_local_poses(shape_matrix))
    rotated = rotate(shape_matrix)
    print(rotated)
    print(get_tile_local_poses(rotated))
