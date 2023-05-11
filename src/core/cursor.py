import pygame as p
from src.constants import BLACK

class Cursor(p.sprite.Sprite):
    def __init__(self, radius):
        p.sprite.Sprite.__init__(self)
        self.image = p.Surface((radius, radius))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.image.fill(BLACK)
    
    def hand(self, sg: p.sprite.Group):
        if p.sprite.spritecollide(self, sg, False):
            p.mouse.set_cursor(p.SYSTEM_CURSOR_HAND)
        else:
            p.mouse.set_cursor(p.SYSTEM_CURSOR_ARROW)