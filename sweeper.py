import pygame as pg
import sys, random
from tile import Tile
from math import floor

pg.init()  # initialize pygame modules


# Return surface with requested size (resizes tiles for width/height)
def get_tiles(size=(1, 1), img=None, width_px=None, height_px=None):
    # if width_px is None or height_px is None:
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


def get_tile_clicked(pos):
    x, y = pos
    surf = pg.display.get_surface()
    s_width = surf.get_width()
    s_height = surf.get_height()
    t_width, t_height = tile_size
    xt = floor(x / (s_width / t_width))
    yt = floor(y / (s_height / t_height))
    # print(f"Screen: {s_width}, {s_height}")
    # print(f"Tiles: {t_width}, {t_height}")
    # print(f"Click: {x}, {y}")
    # print(f"Return: {xt}, {yt}")
    return tiles[yt][xt]

# Get the tile at position clicked
#def get_tile(pos):
#    x, y = pos
#    xt, yt = get_tile_clicked(tile_size, x, y)
#s    return t


def increment_mines(add_list):
    for tile in add_list:
        try:
            tile.num_mines += 1
        except:
            pass

def set_mines(tile_set, num_mines):
    tiles_flat = [t for tl in tile_set for t in tl]
    random.shuffle(tiles_flat)
    for t in tiles_flat[:num_mines]:
        t.is_mine = True

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

    
    for tl_i, t_list in enumerate(tile_set):
        for t_i, t in enumerate(t_list):
            if not t.is_mine:
                continue

            increment = []
            for x, y in index_mods:
                if t_i + x < 0 or t_i + x >= len(t_list):
                    continue
                if tl_i + y < 0 or tl_i + y >= len(tile_set):
                    continue
                increment.append((x, y))

            for mx, my in increment:
                #print(t, mx, my)
                tile_set[tl_i + my][t_i + mx].num_mines += 1

            '''    
            add_list = (
                tile_set[tl_i - 1][t_i - 1 : t_i + 2]
                + t_list[t_i - 1 : t_i + 2 : 2]
                + tile_set[tl_i + 1][t_i - 1 : t_i + 2]
            )
            increment_mines(add_list)
            '''
    

game_over = False

# size = width, height = 1080, 720
tile_img = pg.image.load("imgs/tile.png")
tile_mine = pg.image.load("imgs/tile_mine.png")
tile_flag = pg.image.load("imgs/tile_flag.png")

tile_nums = {}

for i in range(9):
    tile_nums[i] = pg.image.load(f"imgs/tile_{i}.png")


tile_size = 18, 20
tiles = get_tiles(tile_size, tile_img)
screen = draw_tiles(tile_img, tiles)

num_mines = 75
set_mines(tiles, num_mines)

while 1:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        if game_over:
            continue

        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            t = get_tile_clicked(pos)
            if event.button == 1 and not t.flagged:    
                t.clicked = True
                print(t)
                if t.is_mine:
                    screen.blit(tile_mine, t)
                    game_over = True
                else:
                    # if 0, get_tile_clicked recursively for surrounding tiles
                    screen.blit(tile_nums[t.num_mines], t)
                    
            if event.button == 3 and not t.clicked:
                if t.flagged:
                    t.flagged = False
                else:
                    t.flagged = True
                screen.blit(tile_flag, t)


    pg.display.flip()


# notes for next time:
# - Probably put tile functions in tile or grid class
