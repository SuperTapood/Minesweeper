from colors import *
import pygame


class Cell:
    def __init__(self, i, j, size, font):
        self.text = None
        self.is_flagged = False
        self.index = i
        self.jdex = j
        self.size = int(size)
        self.font = font
        self.color = grey
        self.is_bomb = False
        self.pals = []
        self.is_revealed = False
        self.x = self.index * self.size
        self.y = self.jdex * self.size
        self.text_surf = None
        # TODO: give value, blitting system (text render), get neighbors, reveal function
        return

    def get_pals(self, tile_array):
        pals = []
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                try:
                    assert self.index + i >= 0
                    assert self.jdex + j >= 0
                    pals.append(tile_array[self.index + i][self.jdex + j])
                except IndexError as e:
                    pass
                except AssertionError as e:
                    pass
        pals.remove(self)
        return pals

    def prep(self, tile_array):
        self.pals = self.get_pals(tile_array)
        self.text = "B"
        if not self.is_bomb:
            count = 0
            for pal in self.pals:
                if pal.is_bomb:
                    count += 1
            if count > 0:
                self.text = str(count)
            else:
                self.text = ""
        self.text_surf = self.font.render(self.text, False, (0, 0, 0))
        rect = self.text_surf.get_rect()
        rect.center = (self.x, self.y)
        return

    def render(self, scr):
        pygame.draw.rect(scr, self.color, (self.x, self.y, self.size, self.size), 0)
        if self.is_revealed:
            scr.blit(self.text_surf, (self.x + self.size / 3, self.y - self.size / 10))
        return

    def reveal(self):
        self.is_revealed = True
        if self.is_bomb:
            self.color = red
        else:
            self.color = blue
        if self.text == "":
            for pal in self.pals:
                if not pal.is_revealed:
                    pal.reveal()
        return

    def get_loc(self):
        return [self.index, self.jdex]

    def flag(self):
        self.is_flagged = not self.is_flagged
        if self.color == green:
            self.color = grey
        else:
            self.color = green
        return
    pass
