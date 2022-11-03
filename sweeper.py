import pygame as pg 
import sys, random
from tile import Tile
from math import floor
pg.init() # initialize pygame modules



# Return surface with requested size (resizes tiles for width/height)
def get_tiles(size=(1, 1), img=None, width_px=None, height_px=None):
    #if width_px is None or height_px is None:
    #    screen = pg.display.set_mode(width_px, height_px)
    tile = img
    t_width = tile.get_width()
    t_height = tile.get_height()
    t_rect = tile.get_rect()
    x, y = 0, 0
    grid_w, grid_h = size

    tile_grid = []

    for th in range(grid_h):
        tile_grid.append([])
        for tw in range(grid_w):
            tr = t_rect.move(x, y)
            tile = Tile(tr)
            tile_grid[th].append(tile)
            x += t_width
        x = 0
        y += t_height
    return tile_grid

def draw_tiles(img, tile_grid):
    width = len(tile_grid[0]) * img.get_width()
    height = len(tile_grid) * img.get_height()
    size = width, height
    screen = pg.display.set_mode(size)
    for t_list in tile_grid:
        for tile in t_list:
            screen.blit(img, tile.rect)

    return screen


def get_tile_clicked(tile_size, x, y):
    surf = pg.display.get_surface()
    s_width = surf.get_width()
    s_height = surf.get_height()
    t_width, t_height = tile_size
    xt = floor(x/(s_width/t_width))
    yt = floor(y/(s_height/t_height))
    #print(f"Screen: {s_width}, {s_height}")
    #print(f"Tiles: {t_width}, {t_height}")
    #print(f"Click: {x}, {y}")
    #print(f"Return: {xt}, {yt}")
    
    return xt, yt


def click_tile(pos):
    x, y = pos
    xt, yt = get_tile_clicked(tile_size, x, y)
    t = tiles[yt][xt] 
    print(t)
    if t.clicked:
        return
    t.clicked = True
    screen.blit(tile_act, t)


def set_mines(tile_set, num_mines):
    tiles_flat = [t for tl in tile_set for t in tl]
    random.shuffle(tiles_flat)
    for t in tiles_flat[:num_mines]:
        t.is_mine = True
        screen.blit(tile_mine, t)
        


#size = width, height = 1080, 720
tile_img = pg.image.load('tile.png')
tile_act = pg.image.load('tile_dark.png')
tile_mine = pg.image.load('tile_mine.png')

tile_size = 18, 20
tiles = get_tiles(tile_size, tile_img)
screen = draw_tiles(tile_img, tiles)

num_mines = 75
set_mines(tiles, num_mines)

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        mouse = pg.mouse.get_pressed()
        if mouse[0]:
            pos = pg.mouse.get_pos()
            click_tile(pos)

    pg.display.flip()



# notes for next time:
# - Probably put tile functions in tile or grid class
