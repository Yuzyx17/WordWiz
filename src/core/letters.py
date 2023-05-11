import pygame as pg
import math
from src.constants import *

class Letter(pg.sprite.Sprite):
    def __init__(self, char='', target:vec2 = (25, 25)):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(tilesize)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = target
        self.letter = char

        self.transition_speed = 16
        self.transition_snap = 0
        self.clicked = False
        self.move = self.rect.center
        self.center = self.rect.center
    
    def draw(self, screen: pg.Surface):
        letter = pixelfont.render(self.letter, True, BLACK)
        letter_rect = letter.get_rect()
        letter_rect.centerx = self.rect.w//2
        letter_rect.centery = self.rect.h//2
        self.image.blit(letter, letter_rect)
        screen.blit(self.image, self.rect)
    
    def click(self, target: vec2 = None):
        if target:   
            if pg.mouse.get_pressed()[0] and self.rect.collidepoint(pg.mouse.get_pos()):
                self.clicked = True
                self.center = self.rect.center
                self.move = vec2(target - self.center).normalize()

            if self.clicked:
                dx = abs(target.x - self.rect.centerx)
                dy = abs(target.y - self.rect.centery)
                if  ( dx <= self.transition_speed + self.transition_snap and 
                      dy <= self.transition_speed + self.transition_snap):
                    self.rect.centerx, self.rect.centery = target
                    self.clicked = False
                elif self.rect.centerx != target.x and self.rect.centery != target.y:
                    self.center += self.move * self.transition_speed
                    self.rect.center = round(self.center.x), round(self.center.y)
