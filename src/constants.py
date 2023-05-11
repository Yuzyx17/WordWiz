from pygame import Font as ft
from pygame import Vector2 as vec2
import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

pg.font.init()

SIZE = vec2(600, 550)
TITLE = "WordWiz"
tilesize = vec2(64, 64)
pixelfont = ft(r'assets/font/pixelfont.ttf', int(tilesize.x))

alpha = 'abcdefghijklmnopqrstuvwxyz'

def getLetterIndex(letter):
    return ord(letter) - ord('a')

def defaultValue():
    return None
