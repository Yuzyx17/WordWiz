from src.constants import *
from pygame.constants import *
from src.core.letters import Letter
from src.core.cursor import Cursor
from src.core.board import Board

import pygame as pg
import sys

def init_game():
    pg.init()
    
    canvas = pg.display.set_mode(SIZE)
    pg.display.set_caption(TITLE)
    clock = pg.time.Clock()

    board = Board(canvas)
    board.update_pool("abedefghij")

    cursor = Cursor(10)
    player = True
    while True:
        canvas.fill(PURPLE)
        board.draw()

        cursor.reset()
        if player:
            
            if board.spell:
                cursor.hand([board.letter_used, board.letter_pool])
            else:
                cursor.hand([board.letter_used])

        for event in pg.event.get():
            if event.type == QUIT:
                sys.exit()

            if player:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        board.click = True
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        board.click = False
                board.events(event)

        pg.display.flip()
        clock.tick(120)