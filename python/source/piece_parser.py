import sys
import os
from piece import PieceOld

k_piece_ended_format_code = "\n\n"


def load_pieces_from_file(file_name):
    pieces = []
    file_path = os.path.join(sys.path[0], "..\data", file_name)
    with open(file_path, "r") as f:
        content = f.read()
        start_pos = 0
        while content.find(k_piece_ended_format_code, start_pos) != -1:
            last_pos = content.find(k_piece_ended_format_code, start_pos)
            piece_str = content[start_pos : last_pos + 1]
            start_pos = last_pos + len(k_piece_ended_format_code)
            piece = PieceOld()
            piece.set_from_string(piece_str)
            pieces.append(piece)
    return pieces
