from colors import *
import pygame

class Cell:

    def __init__(self, i, j, size, font):
        hidden = pygame.image.load(r'C:\Users\yoavo\Documents\GitHub\Minesweeper\imgs\hidden.png')
        self.hidden = pygame.transform.scale(hidden, (45, 45))
        unhidden = pygame.image.load(r'C:\Users\yoavo\Documents\GitHub\Minesweeper\imgs\unhidden.png')
        self.unhidden = pygame.transform.scale(unhidden, (45, 45))
        flaged = pygame.image.load(r'C:\Users\yoavo\Documents\GitHub\Minesweeper\imgs\flag.png')
        self.flaged = pygame.transform.scale(flaged, (45, 45))
        bomb = pygame.image.load(r'C:\Users\yoavo\Documents\GitHub\Minesweeper\imgs\bomb.png')
        self.bomb = pygame.transform.scale(bomb, (45, 45))
        self.text = None
        self.is_flagged = False
        self.column = i
        self.row = j
        self.size = int(size)
        self.font = font
        self.color = grey
        self.is_bomb = False
        self.pals = []
        self.is_revealed = False
        self.x = self.column * self.size
        self.y = self.row * self.size
        self.text_surf = None
        self.probs = []
        self.prob = 0
        return

    def get_pals(self, tile_array):
        pals = []
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                try:
                    assert self.column + i >= 0
                    assert self.row + j >= 0
                    pals.append(tile_array[self.column + i][self.row + j])
                except IndexError as e:
                    pass
                except AssertionError as e:
                    pass
        pals.remove(self)
        return pals

    def prep(self, tile_array):
        self.pals = self.get_pals(tile_array)
        self.text = "B"
        count = 0
        if not self.is_bomb:
            for pal in self.pals:
                if pal.is_bomb:
                    count += 1
            if count > 0:
                self.text = str(count)
            else:
                self.text = ""
        color = (0, 0, 0)
        if count == 1:
            color = blue
        elif count == 2:
            color = dark_green
        elif count == 3:
            color = red
        elif count == 4:
            color = dark_blue
        elif count == 5:
            color = dark_red
        self.text_surf = self.font.render(self.text, False, color)
        rect = self.text_surf.get_rect()
        rect.center = (self.x, self.y)
        return

    def render(self, scr):
        if self.is_revealed:
            if self.is_bomb:
                scr.blit(self.bomb, (self.x, self.y))
            else:
                scr.blit(self.unhidden, (self.x, self.y))
                scr.blit(self.text_surf, (self.x + self.size / 3, self.y - self.size / 10))
        elif self.is_flagged:
            scr.blit(self.flaged, (self.x, self.y))
        else:
            scr.blit(self.hidden, (self.x, self.y))
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
        return [self.column, self.row]

    def flag(self):
        self.is_flagged = not self.is_flagged
        if self.color == green:
            self.color = grey
        else:
            self.color = green
        return
    pass
