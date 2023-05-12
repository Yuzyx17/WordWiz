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

class Agents(Enum):
    PLAYER = 0
    AI = 1

class BoardState():
    def __init__(self):
        self.pool = dict(zip((i for i in range(10)), (' ' for _ in range(10))))
        self.guesses: List[List[dict | str]] = []
        self.word = None
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

    def can_spell_guess(self):
        try:
            self.index = self.guesses[self.attempt].index(' ')
            return True
        except Exception as e:
            return False

    def spell_guess(self, key, val):
        self.index = self.guesses[self.attempt].index(' ')
        self.guesses[self.attempt][self.index] = {key: val}
        self.pool[key] = ' '

    def undo_guess(self, key, val):
        index = self.guesses[self.attempt].index({key: val})
        self.guesses[self.attempt][index] = ' '
        self.pool[key] = val

    def verify_guess(self):
        return self.trie.search(self.wordify_guess())
    
    def wordify_guess(self):
        return "".join([list(x.values())[0] if type(x) == dict else '' for x in self.guesses[self.attempt]])

    def accept_guess(self):
        self.index = 0
        self.attempt += 1
    
    def get_attempts(self):
        return 6 - self.attempt

class Board():
    def __init__(self, canvas):
        self.state = BoardState()

        self.canvas = canvas
        self.spell = True   #if player is allowed to spell
        self.click = True   #for detecting clicks; communicates from events
        self.pool = ""

        self.player_score = 0
        self.ai_score = 0

        self.turn = Agents.PLAYER
        self.mode = Mode.CODEBREAKER
        
        self.letter_pool = pg.sprite.Group()
        self.letter_used = pg.sprite.Group()
        self.word_guessed = pg.sprite.Group()

    def update_pool(self, pool = None):
        if len(pool) > 10:
            return
        self.pool = pool
        self.letter_pool.empty()
        self.letter_used.empty()
        self.state.reset_state()

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

        if self.turn == Agents.PLAYER and self.mode == Mode.CODEBREAKER:
            self.player_codebreaker()
        elif self.turn == Agents.PLAYER and self.mode == Mode.MASTERMIND:
            self.player_mastermind()
        elif self.turn == Agents.AI and self.mode == Mode.MASTERMIND:
            self.ai_mastermind()
        elif self.turn == Agents.AI and self.mode == Mode.CODEBREAKER:
            self.ai_codebreaker()
 
    def player_codebreaker(self):
        #TRIAL ONLY FOR WHEN TURN = PLAYER and MODE = CODEBREAKER
        self.spell = self.state.can_spell_guess()  #if current board state allows for spelling
        
        letter: Letter
        for letter in self.letter_pool:         #for letters in the pool
            if not letter.clicked and letter not in self.letter_used:
                if letter.click(self.spell and self.click, vec2(letter.rect.left, 250)):
                    #State update
                    attempted_index = self.letter_pool.sprites().index(letter)
                    self.state.spell_guess(attempted_index, letter.letter)
                    self.letter_used.add(letter)   
                    self.click = False
                    break

        for letter in self.letter_used:         #for letters used
            if not letter.clicked:
                if letter.click(True and self.click, vec2(letter.rect.left, 25)):
                    #State update
                    attempted_index = self.letter_pool.sprites().index(letter)
                    self.state.undo_guess(attempted_index, letter.letter)
                    self.letter_used.remove(letter) 
                    self.click = False
                    break
    
    def player_mastermind(self):
        ...
    
    def ai_codebreaker(self):
        ...

    def ai_mastermind(self):
        ...

    def events(self, event):
        ...