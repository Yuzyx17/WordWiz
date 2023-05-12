import pygame as pg

from src.core.letters import Letter
from src.constants import defaultValue
from src.constants import *
from src.utils.trie import Trie

from enum import Enum
from typing import List
from collections import defaultdict

class Mode(Enum):
    CODEBREAKER = 0
    MASTERMIND = 1


class BoardState():
    def __init__(self):
        self.mode = None
        self.pool = dict(zip((i for i in range(10)), (' ' for _ in range(10))))
        self.guesses: List[List[dict | str]] = []
        self.hints = defaultdict(defaultValue)
        self.trie = Trie()
        self.attempt = 0 #row
        self.index = 0 #col
        
        for _ in range(6):
            guess = []
            for i in range(5):
                guess.append(' ')
            self.guesses.append(guess)

        self.trie.save()
        self.trie.load()

    
    def reset_state(self):
        self.pool = dict(zip((i for i in range(10)), (' ' for _ in range(10))))
        self.guesses: List[List[dict | str]] = []
        self.hints = defaultdict(defaultValue)
        self.trie = Trie()
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

    def undo(self, key, val):
        index = self.guesses[self.attempt].index({key: val})
        self.guesses[self.attempt][index] = ' '
        self.pool[key] = val

    def verify(self):
        return self.trie.search(self.wordify())
    
    def wordify(self):
        return "".join([list(x.values())[0] if type(x) == dict else '' for x in self.guesses[self.attempt]])
    
    def guess(self):
        self.index = 0
        self.attempt += 1

class Board():
    def __init__(self, canvas):
        self.canvas = canvas
        self.spell = True   #if player is allowed to spell
        self.click = True   #for detecting clicks; communicates from events
        self.pool = ""

        self.player_score = 0
        self.ai_score = 0

        self.turn = True

        self.state = BoardState()
        self.state.mode = Mode.CODEBREAKER
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
        self.letter_pool.draw(self.canvas)      #drawing pool of letters
        self.letter_used.draw(self.canvas)      #drawing spell attempt
        self.word_guessed.draw(self.canvas)     #drawing guesses

        self.letter_pool.update()
        self.letter_used.update()

        spellable = self.state.spellable()      #if current board state allows for spelling
        self.spell = spellable
            
        letter: Letter
        for letter in self.letter_pool:         #for letters in the pool
            if not letter.clicked and letter not in self.letter_used:
                if letter.click(self.spell and self.click, vec2(letter.rect.left, 250)):
                    attempted_index = self.letter_pool.sprites().index(letter)
                    self.state.spell(attempted_index, letter.letter)
                    self.letter_used.add(letter)   
                    print(self.state.verify(), self.state.wordify())
                    break

        for letter in self.letter_used:         #for letters used
            if not letter.clicked:
                if letter.click(True and self.click, vec2(letter.rect.left, 25)):
                    attempted_index = self.letter_pool.sprites().index(letter)
                    self.state.undo(attempted_index, letter.letter)
                    self.letter_used.remove(letter)
                    break
                    
        if self.click:
            self.click = False
    
    def events(self, event):
        ...