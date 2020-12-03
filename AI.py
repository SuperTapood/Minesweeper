from board import Board
import numpy as np


def find_active_board(tile_array):
    # find the active cells in the board:
    out = []
    for row in tile_array:
        for tile in row:
            if tile.is_revealed or tile.is_flagged:
                out.append(tile)
    return out


def move(tile_array):
    active_cells = find_active_board(tile_array)
    boards = Board(active_cells, tile_array).generate_boards()
    total = len(boards)
    probs = np.zeros(boards[0][0].size)
    for board in boards:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j].is_flagged:
                    probs[i][j] += 1
    max_prob = 0
    cell = None
    for i in range(len(probs)):
        for j in range(len(probs[i])):
            if probs[i][j] > max_prob:
                max_prob = probs[i][j]
                cell = (i, j)
    i, j = cell
    return tile_array[i][j]







