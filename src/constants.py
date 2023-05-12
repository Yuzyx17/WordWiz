import pygame as pg

from pygame import Font as ft
from pygame import Vector2 as vec2
from pygame import Color

WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
CYAN = BLUE + GREEN
MAGENTA = RED + BLUE
YELLOW = RED + GREEN

OFFWHITE = Color(225, 200, 225)

pg.font.init()

SIZE = vec2(650, 550)
TITLE = "WordWiz"
tilesize = vec2(64, 64)
pixelfont = ft(r'assets/font/pixelfont.ttf', int(tilesize.x))

alpha = 'abcdefghijklmnopqrstuvwxyz'

def getLetterIndex(letter):
    return ord(letter) - ord('a')

def defaultValue():
    return None
