from random import randint

first = True
move_count = 0

def reveal(tile):
    pass


def move(current_board):
    global first, move_count
    if first:
        first = False
        i = randint(0, len(current_board) - 1)
        j = randint(0, len(current_board[i]) - 1)
        return current_board[i][j]
    move_count += 1
    if move_count >= 2:
        return
    for arr in current_board:
        for tile in arr:
            if tile.is_revealed and tile.text != "":
                pals = tile.get_pals(current_board)
                left_bombs = int(tile.text)
                undis_pals = 0
                for pal in pals:
                    if not pal.is_revealed:
                        undis_pals += 1
                if left_bombs == undis_pals:
                    for pal in pals:
                        if not pal.is_revealed:
                            pal.flag()

    for arr in current_board:
        for tile in arr:
            if tile.is_revealed and tile.text != "":
                pals = tile.get_pals(current_board)
                left_bombs = int(tile.text)
                flag_pals = 0
                for pal in pals:
                    if not pal.is_flagged:
                        flag_pals += 1
                if left_bombs == flag_pals:
                    for pal in pals:
                        if not pal.is_revealed:
                            pal.reveal()
