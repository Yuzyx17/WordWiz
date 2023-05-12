from src.constants import *
from collections import defaultdict

class Button(pg.sprite.Sprite):
    def __init__(self, size: vec2, color: pg.Color, surface:pg.surface=None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(size) if surface is None else surface
        self.rect = self.image.get_rect()
        self.callback = None
        self.list = None
        self.dict = None

        self.click = False
    
    def update(self, click):
        self.click = click
        if self.click and self.rect.collidepoint(pg.mouse.get_pos()):
            self.callback(*self.list, **self.dict)

        if self.click:
            self.click = False

    def on_click(self, callback, *args, **kwargs):
        self.callback = callback
        self.list = args
        self.dict = kwargs