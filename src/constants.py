import pygame as pg

from pygame import Font as ft
from pygame import Vector2 as vec2
from pygame import Color
from enum import Enum

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

tilesize = vec2(48, 48)
YGAP = 5
XGAP = 10

IPP = vec2((SIZE.x//2)-(XGAP*2)-(tilesize.x*2)-(tilesize.x//2), SIZE.y - (tilesize.y*2) - (YGAP*4))

pixelfont = ft(r'assets/font/pixelfont.ttf', int(tilesize.x))
pixelfont_md = ft(r'assets/font/pixelfont.ttf', int(tilesize.x)//2)
pixelfont_av = ft(r'assets/font/pixelfont.ttf', int(tilesize.x)//3)
pixelfont_sm = ft(r'assets/font/pixelfont.ttf', int(tilesize.x)//4)

alpha = 'abcdefghijklmnopqrstuvwxyz'

WORD_GUESSED_PENALTY = -5
NO_GUESS_PENALTY = -10
WORD_GUESSED_REWARD = 10
NO_GUESS_REWARD = 5
ATTEMPTS_REWARD = 5

AI_WORD_POOL_DIFFICULTY = 100
PLAYER_POOL_DIFFICULTY = 200

def getLetterIndex(letter):
    return ord(letter) - ord('a')

def defaultValue():
    return None

def get_pool_pos(i, gap=1):
    return vec2(IPP.x+((i%5)*tilesize.x)+((i%5)*XGAP * gap), IPP.y+((i//5)*tilesize.y)+((i//5)*-YGAP  * gap))
def get_cor_pos(i, gap=1):
    return vec2(IPP.x+(i*tilesize.x)+(i*XGAP * gap), 10)
def get_gus_pos(i, j, gap=1):
    return vec2(IPP.x+((i%5)*tilesize.x)+((i%5)*XGAP * gap), IPP.y+((j+2)*-tilesize.y)+(j*-YGAP * gap)+10)

class turns(Enum):
    PCB = 1
    PMM = 2
    ACB = 3
    AMM = 4