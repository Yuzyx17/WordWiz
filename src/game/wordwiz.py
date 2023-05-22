from src.constants import *
from pygame.constants import *

from src.utils.cursor import Cursor
from src.core.board import Board

import pygame as pg
import sys


def init_game():
    pg.mixer.pre_init()
    pg.mixer.init()
    pg.init()

    canvas = pg.display.set_mode(SIZE)
    pg.display.set_caption(TITLE)
    clock = pg.time.Clock()

    board = Board(canvas)
    cursor = Cursor(10)

    while True:
        canvas.fill(OFFWHITE)
        board.draw()
        
        cursor.reset()
        board.click = False
        if board.turn:
            
            if board.spell:
                cursor.hand([board.letter_used, 
                             board.letter_pool, 
                             board.buttons])
            else:
                cursor.hand([board.letter_used, 
                             board.buttons])
        else:
            cursor.hand([board.buttons])    

        for event in pg.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.click = True
            board.events(event)

        pg.display.flip()
        clock.tick(60)