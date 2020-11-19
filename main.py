import pygame
from colors import *
from cell import Cell
from math import *
from random import *
from time import time
from AI import move

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
    global preped
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_cell = int(mouse_pos[0] // (scr_size / size))
            y_cell = int(mouse_pos[1] // (scr_size / size))
            chosen = tile_array[x_cell][y_cell]
            if pygame.mouse.get_pressed()[0]:
                if not chosen.is_revealed and not chosen.is_flagged:
                    if not preped:
                        prep(chosen)
                        preped = True
                    chosen.reveal()
                    if chosen.is_bomb:
                        print("DEAD")
                        for arr in tile_array:
                            for tile in arr:
                                tile.reveal()
            elif pygame.mouse.get_pressed()[2]:
                if not preped or chosen.is_revealed:
                    continue
                chosen.flag()


if __name__ == "__main__":
    start = time()
    pygame.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    scr_size = 800
    scr = pygame.display.set_mode((scr_size, scr_size))
    size = 20
    total_mines = 100
    tile_array = np.empty((size, size), Cell)
    for i in range(size):
        for j in range(size):
            tile_array[i][j] = Cell(i, j, scr_size / size, font)
    end = time() - start
    print(f"boot time - {end} secs")
    preped = False
    # chosen = move(tile_array)
    # prep(chosen)
    # chosen.reveal()
    while True:
        start = time()
        # move(tile_array)
        scr.fill(white)
        detect_events()
        render()
        if preped:
            win = True
            for arr in tile_array:
                for tile in arr:
                    if tile.is_bomb and not tile.is_flagged:
                        win = False
                    if not tile.is_bomb and tile.is_flagged:
                        win = False
            if win:
                print("WIN")
        pygame.display.update()
        end = time() - start
        print(f"frame time - {end} seconds - {1 / end} frames")
