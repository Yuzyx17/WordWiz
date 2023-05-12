from src.constants import *
from pygame.constants import *
from src.core.letters import Letter
from src.core.cursor import Cursor
from src.core.board import Board
from src.utils.button import Button

import pygame as pg
import sys
def hello(*args, **kwargs):
    for arg in args:
        print(arg)
    print(kwargs)

def init_game():
    pg.init()
    
    canvas = pg.display.set_mode(SIZE)
    pg.display.set_caption(TITLE)
    clock = pg.time.Clock()

    board = Board(canvas)
    board.update_pool("abcdefghee")

    button = Button(vec2(100, 50), (100, 150, 200)) #Creating Button
    button.on_click(hello, 2, 's', m="asdasd")      #Attaching callback
    button.rect.x, button.rect.y = vec2(250, 250)   #positioning the button
    grp = pg.sprite.Group()     
    grp.add(button) #adding button to sprite group for cursor handling

    cursor = Cursor(10)

    while True:
        canvas.fill(PURPLE)

        grp.draw(canvas)

        grp.update(board.click)     #sample of attached callback

        board.draw()
       

        cursor.reset()
        if board.turn:
            
            if board.spell:
                cursor.hand([board.letter_used, board.letter_pool])
            else:
                cursor.hand([board.letter_used])

        for event in pg.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.click = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    board.click = False
            board.events(event)

        pg.display.flip()
        clock.tick(120)