import pygame as pg
from collections import Counter
from src.core.letters import Letter
from src.constants import *
from typing import List

class BoardState():
    def __init__(self):
        self.pool = dict(zip((i for i in range(10)), (' ' for _ in range(10))))
        self.guesses: List[List[dict | str]] = []
        self.attempt = 0 #row
        self.index = 0 #col

        for _ in range(6):
            guess = []
            for i in range(5):
                guess.append(' ')
            self.guesses.append(guess)
    
    def spellable(self):
        try:
            self.index = self.guesses[self.attempt].index(' ')
            return True
        except Exception as e:
            return False

    def spell(self, key, val):
        self.index = self.guesses[self.attempt].index(' ')
        self.guesses[self.attempt][self.index] = {key: val}
        self.pool[key] = ' '
        print(f'{self.guesses[self.attempt]}\n {self.pool}')

    def undo(self, key, val):
        index = self.guesses[self.attempt].index({key: val})
        self.guesses[self.attempt][index] = ' '
        self.pool[key] = val
        print(f'{self.guesses[self.attempt]}\n {self.pool}')

    def verify(self, word):
        ...
    
    def wordify(self, guess_index):
        ...
    
    def guess(self):
        self.index = 0
        self.attempt += 1

class Board():
    def __init__(self, canvas):
        self.canvas = canvas
        self.spell = True
        self.click = True
        self.pool = ""

        self.state = BoardState()
        self.letter_pool = pg.sprite.Group()
        self.letter_used = pg.sprite.Group()
        self.word_guessed = pg.sprite.Group()

    def update_pool(self, pool = None):
        if len(pool) > 10:
            return
        self.pool = pool
        self.letter_pool.empty()

        for i in range(len(pool)):
            self.state.pool[i] = self.pool[i]
            letter = Letter(self.state.pool[i])
            letter.rect.x = i*tilesize.x
            self.letter_pool.add(letter)

    def draw(self):
        self.letter_pool.draw(self.canvas)
        self.letter_used.draw(self.canvas)
        self.word_guessed.draw(self.canvas)

        spellable = self.state.spellable()
        self.spell = spellable
            
        letter: Letter
        for letter in self.letter_pool:
            letter.update()
            if not letter.clicked and letter not in self.letter_used:
                if letter.click(self.spell and self.click, vec2(letter.rect.x, 250)):
                    attempted_index = self.letter_pool.sprites().index(letter)
                    self.state.spell(attempted_index, letter.letter)
                    self.letter_used.add(letter)          

        for letter in self.letter_used:
            letter.update()
            if not letter.clicked:
                if letter.click(True and self.click, vec2(letter.rect.x, 25)):
                    attempted_index = self.letter_pool.sprites().index(letter)
                    self.state.undo(attempted_index, letter.letter)
                    self.letter_used.remove(letter)

                    
        if self.click:
            self.click = False
    
    def events(self, event):
        ...