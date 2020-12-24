import numpy as np
import pygame
from colors import *
from AI import move as mov
from random import choice


def freeze(tile_array, scr, size, scr_size):
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


def get_root(board):
    for col in board:
        for tile in col:
            if not tile.is_revealed and not tile.is_flagged:
                return tile


truthers = []
checked = []


def get_truthers(root, board):
    global truthers, checked
    if root not in checked:
        checked.append(root)
        pals = root.get_pals(board)
        for pal in pals:
            if pal.is_revealed:
                if pal not in truthers:
                    truthers.append(pal)
            elif not pal.is_flagged:
                get_truthers(pal, board)
    return


def set_board(inc, sus):
    for i in range(len(sus)):
        sus[i].pred = inc[i]
    return


def is_valid_board(truth, board) -> bool:
    for t in truth:
        bombs = int(t.text) - sum(
            1 for pal in t.get_pals(board) if pal.is_flagged or pal.pred == 1
        )
        if bombs != 0:
            return False
    return True


def reset_board(sus):
    for s in sus:
        s.pred = 0
    return


def increment(inc):
    for i in range(len(inc)):
        if inc[i] == 1:
            inc[i] = 0
        else:
            inc[i] = 1
            return inc
    return None


def copy_board(inc):
    return [i for i in inc]


def get_probs(boards):
    probs = []
    for j in range(len(boards[0])):
        prob = sum(boards[i][j] for i in range(len(boards)))
        probs.append(prob)
    for prob_ in probs:
        prob_ /= len(boards)
    return probs


def get_best_guess(probs, sus):
    # let's get the certainties out of the way
    low_index = 0
    lowest = 1.0
    for i, p in enumerate(probs):
        if p == 0.0:
            tile = sus[probs.index(p)]
            tile.reveal()
            return tile
        elif p == 1.0:
            tile = sus[probs.index(p)]
            tile.flag()
            return tile
        else:
            if p < lowest:
                low_index = i
    tile = sus[low_index]
    tile.reveal()
    return tile


def move(board, scr, size, scr_size):
    global truthers
    moved, curpos = mov(board)
    if moved == "False":
        print("resorting")
        og = get_root(board)
        # og.is_bomb = True
        # og.is_revealed = True
        get_truthers(og, board)
        sus = []
        for t in truthers:
            for pal in t.get_pals(board):
                if (
                    not pal.is_revealed
                    and not pal.is_flagged
                    and pal not in sus
                ):
                    sus.append(pal)
        if len(sus) > 20:
            return "False", (0, 0)
        inc = [0 for _ in sus]
        boards = []
        log = []
        while True:
            set_board(inc, sus)
            if is_valid_board(truthers, board):
                boards.append(copy_board(inc))
            reset_board(sus)
            inc = increment(inc)
            if inc is None:
                break
        assert len(sus) > 0
        assert len(truthers) > 0
        try:
            assert len(boards) > 0
        except AssertionError:
            # all probs are equal
            chosen = choice(sus)
            chosen.reveal()
            return True, chosen.get_loc()
        probs = get_probs(boards)
        best = get_best_guess(probs, sus)
        return True, best.get_loc()
    return moved, curpos
