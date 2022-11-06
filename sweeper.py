import pygame as pg
from tile import Tile, TileSet, TileImgs
import sys

def draw_tiles(img, tile_set):
    width = tile_set.size_x * img.get_width()
    height = tile_set.size_y * img.get_height()
    size = width, height
    screen = pg.display.set_mode(size)
    for t_list in tile_set.grid:
        for tile in t_list:
            screen.blit(img, tile.rect)

    return screen

def click_tile(tile):
    tile.clicked = True
    screen.blit(TileImgs.nums[tile.num_mines], tile)
    if tile.num_mines == 0:
        t_near = tile_set.get_tiles_near(tile.x, tile.y)
        #print(t_near)
        for t in t_near:
            #screen.blit(TileImgs.nums[t.num_mines], t)
            #print(t_near)
            if not t.clicked:
                print(f'Click tile: {t.x}, {t.y}')
                click_tile(t)

pg.init()  # initialize pygame modules
game_over = False
tile_set = TileSet(20, 20, 75)
screen = draw_tiles(TileImgs.reg, tile_set)



while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        if game_over:
            continue

        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            t = tile_set.get_tile_clicked(pos, pg.display.get_surface())
            if event.button == 1 and not t.flagged:    
                #t.clicked = True
                #print(t)
                if t.is_mine:
                    for m in tile_set.mines:
                        screen.blit(TileImgs.mine, m)
                    screen.blit(TileImgs.mine_click, t)
                    game_over = True
                else:
                    # if 0, get_tile_clicked recursively for surrounding tiles
                    click_tile(t)

                    
            if event.button == 3 and not t.clicked:
                if t.flagged:
                    t.flagged = False
                    screen.blit(TileImgs.reg, t)
                else:
                    t.flagged = True
                    screen.blit(TileImgs.flag, t)


    pg.display.flip()


# notes for next time:
# - Probably put tile functions in tile or grid class
