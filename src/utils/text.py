import pygame as pg
from pygame.math import Vector2 as vec2
from src.constants import *

class TextRenderer(pg.sprite.Sprite):
    def __init__(self, size: vec2, pos: vec2 = vec2(0, 0), text="",color = BLACK):
        pg.sprite.Sprite.__init__(self)
        self.text = text
        self.change = True
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect()
        self.image.fill(color)
        self.image.set_colorkey(color)
        self.rect.topleft = pos
        self.color = color
        self.setVisible = True

    def update(self, color=(15, 15, 15)):
        if not self.setVisible:
            self.image.fill(self.color)
        # print(self.text)
        if self.change:
            self.image.fill(self.color)
            text = pixelfont_sm.render(self.text, True, color)
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.w//2
            text_rect.centery = self.rect.h//2
            self.image.blit(text, text_rect)
            self.change = False
    
    def refresh(self):
        self.change = True

    def change_text(self, text):
        self.text = text
        self.change = True

# self.font = pygame.font.SysFont("Arial", size)
# self.textSurf = self.font.render(text, 1, color)
# self.image = pygame.Surface((width, height))
# W = self.textSurf.get_width()
# H = self.textSurf.get_height()
# self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])