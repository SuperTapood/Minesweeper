from random import choice


def move(board):
    global flags, reveals
    for row in board:
        for tile in row:
            if tile.is_revealed:
                if tile.text != "":
                    hidden = []
                    if tile.text == "B":
                        return "B", (0, 0)
                    bombs = int(tile.text)
                    flags = []
                    for tile in tile.get_pals(board):
                        if not tile.is_revealed:
                            if tile.is_flagged:
                                flags.append(tile)
                            else:
                                hidden.append(tile)
                    if len(hidden) == bombs - len(flags):
                        for tile in hidden:
                            tile.flag()
                            return "True", tile.get_loc()
                    if len(flags) == bombs:
                        for tile in hidden:
                            tile.reveal()
                            return "True", tile.get_loc()
    return "False", (0, 0)


def move_rand(board):
    hidden = []
    for row in board:
        for tile in row:
            if not tile.is_revealed:
                hidden.append(tile)
    chosen = choice(hidden)
    chosen.reveal()
    return chosen.get_loc()
