import pygame as pg
from pygame.math import Vector2 as vec2
from src.constants import *

class TextRenderer(pg.sprite.Sprite):
    def __init__(self, size: vec2, color = BLACK):
        pg.sprite.Sprite.__init__(self)
        self.text = ""
        self.change = False
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect()

    def update(self):
        if self.change:
            text = pixelfont_sm.render(self.text, True, BLACK)
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.w//2
            text_rect.centery = self.rect.h//2
            self.image.blit(text, text_rect)
            self.change = False
    
    def change_text(self, text):
        self.text = text
        self.change = True