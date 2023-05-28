from src.constants import *
from collections import defaultdict

class Button(pg.sprite.Sprite):
    def __init__(self, size: vec2, color: pg.Color, surface:pg.surface=None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(size) if surface is None else surface
        self.rect = self.image.get_rect()
        self.fill = color
        self.callback = None
        self.list = None
        self.dict = None
        self.returnValue = None
        self.button_sound = pg.mixer.Channel(1)
        self.button_player = pg.mixer.Sound(butsound)
        self.click = False
        self.emu_click = False
        self.change = False
        self.text = ""
        self.image.fill(self.fill)
    
    def update(self, click):
        if not self.click:    
            self.click = click
        if (self.click and self.rect.collidepoint(pg.mouse.get_pos())) or self.emu_click:
            self.button_sound.set_volume(0.15)
            self.button_sound.play(self.button_player)
            self.returnValue = self.callback(*self.list, **self.dict)
            self.click = False
            self.emu_click = False
        if self.change:
            self.set_text(self.text)
            self.change = False
        self.click = False
        self.emu_click = False

    def emulate_click(self):
        self.emu_click = True

    def change_text(self, text):
        self.text = text
        self.change = True

    def set_text(self, text, color = BLACK):
        self.image.fill(self.fill)
        self.text = text
        text = pixelfont_sm.render(self.text, True, color)
        text_rect = text.get_rect()
        text_rect.centerx = self.rect.w//2
        text_rect.centery = self.rect.h//2
        self.image.blit(text, text_rect)

    def on_click(self, callback, *args, **kwargs):
        self.callback = callback
        self.list = args
        self.dict = kwargs