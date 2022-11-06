import pygame as pg
import sys, random
from math import floor

class TileImgs():
    reg = pg.image.load("imgs/tile.png")
    mine = pg.image.load("imgs/tile_mine.png")
    flag = pg.image.load("imgs/tile_flag.png")
    mine_click = pg.image.load("imgs/tile_mine_click.png")
    nums = {}

    for i in range(9):
        nums[i] = pg.image.load(f"imgs/tile_{i}.png")


class Tile:
    
    def __init__(self, rect, x, y):
        self.clicked = False
        self.flagged = False
        self.is_mine = False
        self.rect = rect
        self.num_mines = 0
        self.x = x # Position in tile grid
        self.y = y

    def __str__(self):
        r = f'Clicked: {self.clicked} Mine: {self.is_mine} Num Mines: {self.num_mines} Flagged: {self.flagged}'
        return r


class TileSet():

    index_mods = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1)
    ]

    def __init__(self, size_x, size_y, num_mines):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = self.get_tiles(size_x, size_y, TileImgs.reg)
        self.num_mines = num_mines
        self.mines = self.set_mines(num_mines)


    # Return surface with requested size (needs to resize tiles for width/height)
    def get_tiles(self, size_x, size_y, img=None, width_px=None, height_px=None):
        # if width_px is None or height_px is None:
        #    self.screen = pg.display.set_mode(width_px, height_px)
        tile = img
        print(tile)
        t_width = tile.get_width()
        t_height = tile.get_height()
        t_rect = tile.get_rect()
        x, y = 0, 0

        grid = []

        for h, th in enumerate(range(size_y)):
            grid.append([])
            for w, tw in enumerate(range(size_x)):
                tr = t_rect.move(x, y)
                tile = Tile(tr, h, w)
                grid[th].append(tile)
                x += t_width
            x = 0
            y += t_height
        return grid


    # Returns the tile at the position
    def get_tile_clicked(self, pos, surface):
        x, y = pos
        s_width = surface.get_width()
        s_height = surface.get_height()
        t_width, t_height = self.size_x, self.size_y
        xt = floor(x / (s_width / t_width))
        yt = floor(y / (s_height / t_height))
        return self.grid[yt][xt]


    # Returns the tiles surrounding a tile
    def get_tiles_near(self, tile_list_i, tile_i):
        tl_i = tile_list_i
        t_i = tile_i
        tiles = []
        for x, y in TileSet.index_mods:
            if t_i + x < 0 or t_i + x >= len(self.grid[0]):
                continue
            if tl_i + y < 0 or tl_i + y >= len(self.grid):
                continue
            tiles.append(self.grid[tl_i+y][t_i+x])
        return tiles


    # Set the minefield and precalculate all tile numbers
    def set_mines(self, num_mines):
        tiles_flat = [t for tl in self.grid for t in tl]
        random.shuffle(tiles_flat)
        self.mines = tiles_flat[:num_mines]

        for t in self.mines:
            t.is_mine = True

        for tl_i, t_list in enumerate(self.grid):
            for t_i, t in enumerate(t_list):
                if not t.is_mine:
                    continue

                tiles_near = self.get_tiles_near(tl_i, t_i)
                for tn in tiles_near:
                    tn.num_mines += 1

        return self.mines    


