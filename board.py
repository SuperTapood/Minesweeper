import numpy as np
from cell import Cell
import copy
from itertools import product


class Board:
    def __init__(self, active_cells, tile_array):
        cells = []
        for cell in active_cells:
            cells.append(cell)
            cell.prob = -1
            for pal in cell.get_pals(tile_array):
                if pal not in cells:
                    cells.append(pal)
        lowest_index = 99999
        highest_index = 0
        lowest_jdex = 99999
        highest_jdex = 0
        for cell in cells:
            if cell.column > highest_index:
                highest_index = cell.column
            if cell.column < lowest_index:
                lowest_index = cell.column
            if cell.row > highest_jdex:
                highest_jdex = cell.row
            if cell.row < lowest_jdex:
                lowest_jdex = cell.row
        index_diff = highest_index - lowest_index
        jdex_diff = highest_jdex - lowest_jdex
        base_board = np.empty((index_diff, jdex_diff), Cell)
        for cell in cells:
            i = cell.column - lowest_index - 1
            j = cell.row - lowest_jdex - 1
            base_board[i][j] = cell
        self.base_board = base_board
        return

    def create_board(self, board):
        arr = np.empty(shape=self.base_board.shape, dtype=Cell)
        for i, row in enumerate(self.base_board):
            for j, cell in enumerate(row):
                ncell = copy.copy(cell)
                if board[i][j] == 1:
                    if cell.is_revealed():
                        return None
                    ncell.flag()
                arr[i][j] = ncell
        return arr

    def generate_boards(self):
        length = self.base_board.shape[0] * self.base_board.shape[1]
        string = "01"
        possible = product(string, repeat=length)
        boards = []
        for board in possible:
            out = self.create_board(board)
            boards.append(out)
