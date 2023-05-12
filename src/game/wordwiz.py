from src.constants import *
from pygame.constants import *

from src.utils.cursor import Cursor
from src.core.board import Board
from src.utils.button import Button

import pygame as pg
import sys


def init_game():
    pg.init()
    
    canvas = pg.display.set_mode(SIZE)
    pg.display.set_caption(TITLE)
    clock = pg.time.Clock()

    board = Board(canvas)
    board.update_pool("abcdefghee")

    #BUTTON SAMPLE
    button = Button(vec2(100, 50), (100, 150, 200))     #Creating Button
    button.on_click(board.guess)    #Attaching callback board.updatepool with arg glassspade
    # button.list = ["helloworld"]                        #Changing args
    button.rect.x, button.rect.y = vec2(450, 250)       #positioning the button
    grp = pg.sprite.Group()     
    grp.add(button) #adding button to sprite group for cursor handling
    #END SAMPLE BUTTON

    cursor = Cursor(10)

    while True:
        canvas.fill(OFFWHITE)

        board.draw()
        grp.draw(canvas)
        grp.update(board.click)     #sample of attached callback

        cursor.reset()
        board.click = False
        if board.turn:
            
            if board.spell:
                cursor.hand([board.letter_used, board.letter_pool, grp])
            else:
                cursor.hand([board.letter_used, grp])

        for event in pg.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.click = True
            board.events(event)

        pg.display.flip()
        clock.tick(60)