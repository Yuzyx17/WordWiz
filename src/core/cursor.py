import pygame as p
from src.constants import BLACK

class Cursor(p.sprite.Sprite):
    def __init__(self, radius):
        p.sprite.Sprite.__init__(self)
        self.image = p.Surface((radius, radius))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.image.fill(BLACK)
        self.colliding = False

    def hand(self, sg):
        self.colliding = False
        sg = p.sprite.Group(sg)
        if p.sprite.spritecollide(self, sg, False):
            self.colliding = True
            p.mouse.set_cursor(p.SYSTEM_CURSOR_HAND)
        sg.empty()
        del sg
        
    
    def reset(self):
        if not self.colliding:
            p.mouse.set_cursor(p.SYSTEM_CURSOR_ARROW)
        self.rect.x, self.rect.y = p.mouse.get_pos()