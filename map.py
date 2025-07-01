import pygame as pg

from settings import *

_ = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, _, _, _, 2, _, _, _, _, _, _, _, 1],
    [1, _, 2, 2, 2, _, 2, 2, 2, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, 1],
    [1, _, 1, 1, 1, _, 1, 1, 1, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class Map:
    def __init__(self, screen):
        self.screen = screen
        self.world_map = {}
        self.world_map_not_wall = []
        self.get_map()

    def get_map(self):
        for j, row in enumerate(mini_map):
            for i, value in enumerate(row):
                if value: self.world_map[(i, j)] = value
                else: self.world_map_not_wall.append((i, j))

    def draw(self):
        for pos in self.world_map:
            pg.draw.rect(self.screen, "darkgray", (pos[0] * CELL_PIXELS, pos[1] * CELL_PIXELS, CELL_PIXELS, CELL_PIXELS), 2)