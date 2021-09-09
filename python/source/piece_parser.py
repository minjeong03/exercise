import sys
import os
from turtle import shapesize

k_piece_ended_format_code = "\n\n"


def load_shape_matrices_from_file(file_name):
    shape_matrices = []
    file_path = os.path.join(sys.path[0], "..\data", file_name)
    with open(file_path, "r") as f:
        content = f.read()
        start_pos = 0
        while content.find(k_piece_ended_format_code, start_pos) != -1:
            last_pos = content.find(k_piece_ended_format_code, start_pos)
            piece_str = content[start_pos : last_pos + 1]
            start_pos = last_pos + len(k_piece_ended_format_code)
            shape_matrix = parse_shape_matrix_from_string(piece_str)
            shape_matrices.append(shape_matrix)
    return shape_matrices


def parse_shape_matrix_from_string(str):
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
    return result

if __name__ == "__main__":
    shape_matrices = load_shape_matrices_from_file("pieces.txt")

    print(shape_matrices[0])
