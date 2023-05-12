from pygame import Font as ft
from pygame import Vector2 as vec2
from enum import Enum
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

SIZE = vec2(650, 550)
TITLE = "WordWiz"
tilesize = vec2(64, 64)
pixelfont = ft(r'assets/font/pixelfont.ttf', int(tilesize.x))

alpha = 'abcdefghijklmnopqrstuvwxyz'

class Mode(Enum):
    CODEBREAKER = 0
    MASTERMIND = 1

class Agents(Enum):
    PLAYER = 0
    AI = 1

def getLetterIndex(letter):
    return ord(letter) - ord('a')

def defaultValue():
    return None
