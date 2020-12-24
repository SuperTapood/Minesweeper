import pygame
from colors import *
from cell import Cell
from math import *
from random import *
from time import time, sleep
from AIV2 import move

import numpy as np


def freeze():
    global tile_array, scr, size, scr_size
    while True:
        for a in tile_array:
            for t in a:
                t.render(scr)
        for k in range(size):
            pygame.draw.line(scr, black, (k * int(scr_size / size), 0),
                             (k * int(scr_size / size), scr_size), 2)
            pygame.draw.line(scr, black, (0, k * int(scr_size / size)),
                             (scr_size, k * int(scr_size / size)), 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.update()


def render():
    for a in tile_array:
        for t in a:
            t.render(scr)
    for k in range(size):
        pygame.draw.line(scr, black, (k * int(scr_size / size), 0),
                         (k * int(scr_size / size), scr_size), 2)
        pygame.draw.line(scr, black, (0, k * int(scr_size / size)),
                         (scr_size, k * int(scr_size / size)), 2)
    return


def prep(first):
    global tile_array
    opts = []
    for i in range(size):
        for j in range(size):
            opts.append([i, j])
    opts.remove(first.get_loc())
    for cell in first.get_pals(tile_array):
        opts.remove(cell.get_loc())
    for _ in range(mines):
        index = int(floor(uniform(0, len(opts))))
        i, j = opts[index]
        opts.pop(index)
        tile_array[i][j].is_bomb = True
    for col in tile_array:
        for tile in col:
            tile.prep(tile_array)
    return


def detect_events():
    global preped, tile_array
    chosen = tile_array[i][j]
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     x_cell = int(mouse_pos[0] // (scr_size / size))
        #     y_cell = int(mouse_pos[1] // (scr_size / size))
        #     chosen = board[x_cell][y_cell]
        #     if pygame.mouse.get_pressed()[0]:
        #         if not chosen.is_revealed and not chosen.is_flagged:
        #             if not preped:
        #                 prep(chosen)
        #                 preped = True
        #             chosen.reveal()
        #             if chosen.is_bomb:
        #                 print("DEAD")
        #                 for arr in board:
        #                     for tile in arr:
        #                         tile.reveal()
        #     elif pygame.mouse.get_pressed()[2]:
        #         if not preped or chosen.is_revealed:
        #             continue
        #         chosen.flag()
    # if state == 1:
    #     # tile is safe
    #     if not chosen.is_revealed and not chosen.is_flagged:
    #         if not preped:
    #             prep(chosen)
    #             preped = True
    #         chosen.reveal()
    #         if chosen.is_bomb:
    #             print("DEAD")
    #             for arr in board:
    #                 for tile in arr:
    #                     tile.reveal()
    # elif state == 2:
    #     if chosen.is_revealed:
    #         return
    #     chosen.flag()
    return


def did_win(board):
    for col in board:
        for tile in col:
            if tile.is_bomb and not tile.is_flagged:
                return False
            if not tile.is_bomb and tile.is_flagged:
                return False
    return True


def did_lose(board):
    for col in board:
        for tile in col:
            if tile.is_bomb and tile.is_revealed:
                return True
    return False


def reveal_all(tiles):
    for col in tiles:
        for tile in col:
            tile.reveal()
    return


def is_all_revealed(board):
    for col in board:
        for tile in col:
            if not tile.is_revealed and not tile.is_flagged:
                return False
    return True


def reset_board(board):
    for col in board:
        for tile in col:
            tile.is_revealed = False
            tile.is_flagged = False
    return


if __name__ == "__main__":
    diffs = {}
    pygame.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    scr_size = 800
    scr = pygame.display.set_mode((scr_size, scr_size))
    size = int(scr_size / 40)
    mines_percentage = 15
    mines = int((mines_percentage / 100) * (size * size))
    mines = 60
    cursor = pygame.image.load("imgs/cursor.png")
    cursor = pygame.transform.scale(cursor, (28, 40))
    lost = 0
    win = 0
    while True:
        tile_array = np.empty((size, size), Cell)
        for i in range(size):
            for j in range(size):
                tile_array[j][i] = Cell(j, i, scr_size / size, font)
        # # IMPORTANT!!
        # # board[col][row]
        prep(tile_array[int(size / 2)][int(size / 2)])
        tile_array[int(size / 2)][int(size / 2)].reveal()
        while True:
            scr.fill(white)
            detect_events()
            render()
            if did_win(tile_array):
                print("WIN")
                win += 1
                try:
                    print(f"win lose ratio: {win / lost}")
                except:
                    pass
                break
            elif did_lose(tile_array):
                print("LOST")
                lost += 1
                try:
                    print(f"win lose ratio: {win / lost}")
                except:
                    pass
                break
            moved, curpos = move(tile_array, scr, size, scr_size)
            if moved == "False":
                print("so many boards")
                break
            elif moved == "unsolve":
                print("board is unsolvable?")
                freeze()
                break
            # if moved == "False":
            #     print("STUCK")
            #     curpos = move_rand(board=tile_array)
            # elif moved == "B":
            #     print("LOSE")
            #     break
            x, y = curpos
            scr.blit(cursor, (x * 40 + 10, y * 40 + 10))
            pygame.display.update()
