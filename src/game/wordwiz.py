from src.constants import *
from pygame.constants import *
from src.core.letters import Letter
from src.core.cursor import Cursor

import pygame as pg
import sys

def init_game():
    pg.init()

    canvas = pg.display.set_mode(SIZE)
    pg.display.set_caption(TITLE)
    clock = pg.time.Clock()
    
    letters = pg.sprite.Group()
    for i in range(len(TITLE)):
        letter = Letter(TITLE[i])
        letter.rect.x = i*tilesize.x
        letters.add(letter)

    cursor = Cursor(10)
    dragging = False
    while True:
        canvas.fill(PURPLE)
        cursor.rect.x, cursor.rect.y = pg.mouse.get_pos()

        for event in pg.event.get():
            if event.type == QUIT:
                sys.exit()

        letters.draw(canvas)

        letter: Letter
        for letter in letters:
            letter.draw(canvas)
            letter.click(vec2(SIZE.x//2, SIZE.y//2))

        cursor.hand(letters)

        pg.display.flip()
        clock.tick(120)