import pygame
from colors import *
from cell import Cell
from math import *
from random import *
from time import time, sleep
from AI import move, move_rand

# todo: add 4 difficulties (test, easy, med, hard), fix solver and make it work


import numpy as np


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
    for n in range(total_mines):
        index = int(floor(uniform(0, len(opts))))
        i, j = opts[index]
        opts.pop(index)
        tile_array[i][j].is_bomb = True
    for arr in tile_array:
        for tile in arr:
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
        #     chosen = tile_array[x_cell][y_cell]
        #     if pygame.mouse.get_pressed()[0]:
        #         if not chosen.is_revealed and not chosen.is_flagged:
        #             if not preped:
        #                 prep(chosen)
        #                 preped = True
        #             chosen.reveal()
        #             if chosen.is_bomb:
        #                 print("DEAD")
        #                 for arr in tile_array:
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
    #             for arr in tile_array:
    #                 for tile in arr:
    #                     tile.reveal()
    # elif state == 2:
    #     if chosen.is_revealed:
    #         return
    #     chosen.flag()
    return


def did_win(tile_array):
    for arr in tile_array:
        for tile in arr:
            if tile.is_bomb and not tile.is_flagged:
                return False
            if not tile.is_bomb and tile.is_flagged:
                return False
    return True


if __name__ == "__main__":
    pygame.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    scr_size = 800
    scr = pygame.display.set_mode((scr_size, scr_size))
    size = 20
    total_mines = 60
    cursor = pygame.image.load("imgs/cursor.png")
    cursor = pygame.transform.scale(cursor, (28, 40))
    while True:
        tile_array = np.empty((size, size), Cell)
        for i in range(size):
            for j in range(size):
                tile_array[j][i] = Cell(j, i, scr_size / size, font)
        # # IMPORTANT!!
        # # tile_array[row][col]
        prep(tile_array[10][10])
        tile_array[10][10].reveal()
        while True:
            scr.fill(white)
            detect_events()
            render()
            if did_win(tile_array):
                print("WIN")
                break
            sleep(0.01)
            moved, curpos = move(board=tile_array)
            if moved == "False":
                print("STUCK")
                curpos = move_rand(board=tile_array)
            elif moved == "B":
                print("LOSE")
                break
            x, y = curpos
            scr.blit(cursor, (x * 40 + 10, y * 40 + 10))
            pygame.display.update()
