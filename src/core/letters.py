import pygame as pg
from src.constants import *

class Letter(pg.sprite.Sprite):
    def __init__(self, char=' ', index = 0, target:vec2 = (25, 25)):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(tilesize)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = target
        self.letter = char
        self.index = index

        self.transition_speed = 60
        self.transition_snap = 30
        self.clicked = False
        self.move = vec2(self.rect.topleft)
        self.pos = vec2(self.rect.topleft)
        self.target = vec2()

        self.draw()
    
    def draw(self):
        letter = pixelfont.render(self.letter, True, BLACK)
        letter_rect = letter.get_rect()
        letter_rect.centerx = self.rect.w//2
        letter_rect.centery = self.rect.h//2
        self.image.blit(letter, letter_rect)

    def snap(self):
        dx = abs(self.target.x - self.rect.x)
        dy = abs(self.target.y - self.rect.y)
        if (dx <= self.transition_speed + self.transition_snap and 
            dy <= self.transition_speed + self.transition_snap):
            self.rect.x, self.rect.y = self.target
            self.clicked = False

    def update(self):
        if self.clicked:
            self.snap()
            if not self.clicked: return
            self.pos.x += self.move.x * self.transition_speed
            self.pos.y += self.move.y * self.transition_speed
            self.rect.topleft = round(self.pos.x), round(self.pos.y)

    def translate(self, target: vec2 = None):
        if target != self.rect.topleft and self.clicked:
            self.pos = vec2(self.rect.topleft)
            self.move = vec2(target - self.pos).normalize()
            self.target = target

    def emulated_click(self):
        self.clicked = True
        return self.clicked

    def click(self, clickable=False):
        if clickable and self.rect.collidepoint(pg.mouse.get_pos()):
            self.clicked = True
        return self.clicked


        
