import pygame as pg

from src.constants import *
from src.core.letters import Letter
from src.game.player import Player
from src.game.ai import AI
from src.utils.trie import Trie

from typing import List
from collections import defaultdict

#############################################################
# self.ai.score        self.word        self.player.score   #
#               self.guesses[attempts][5]                   #
#               self.guesses[attempts][4]                   #
#               self.guesses[attempts][3]                   #
#               self.guesses[attempts][2]                   #
#               self.guesses[attempts][1]                   #
#               self.guesses[attempts][0]                   #
#                     self.pool % 5                         #
#                     self.pool % 5         self.button     #
#############################################################

class BoardState():
    def __init__(self):
        self.pool = dict(zip((i for i in range(10)), (' ' for _ in range(10))))
        self.guesses: List[List[dict | str]] = []
        self.word = None
        self.hints = defaultdict(defaultValue)
        self.trie = Trie()
        self.win = False
        self.attempts = []
        self.attempt = 0 #row
        self.index = 0 #col
        
        for _ in range(6):
            guess = []
            for i in range(5):
                guess.append(' ')
            self.guesses.append(guess)

        self.trie.save()
        self.trie.load()

    def reset(self):
        self.pool = dict(zip((i for i in range(10)), (' ' for _ in range(10))))
        self.guesses: List[List[dict | str]] = []
        self.word = "faced"
        self.hints = defaultdict(defaultValue)
        self.win = False
        self.attempts = []
        self.attempt = 0 #row
        self.index = 0 #col
        
        for _ in range(6):
            guess = []
            for _ in range(5):
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
        return self.index
        
    def undo_guess(self, key, val):
        index = self.guesses[self.attempt].index({key: val})
        self.guesses[self.attempt][index] = ' '
        self.pool[key] = val
        return index

    def verify_guess(self):
        return self.trie.search(self.wordify_guess())
    
    def wordify_guess(self):
        return "".join([list(x.values())[0] if type(x) == dict else '' for x in self.guesses[self.attempt]])

    def accept_guess(self):
        word_guess = self.wordify_guess()
        #check if already attempted
        if not self.verify_guess(): return False
        if word_guess in self.attempts: return False
        if word_guess == self.word: self.win = True
        self.attempts.append(word_guess)
        #check win condition
        for index in range(5):
            if self.word[index] == word_guess[index]:
                self.hints[index] = self.word[index]

        self.index = 0
        self.attempt += 1

        return True
    
    def get_guess_attempts(self):
        return 6 - self.attempt

class Board():
    def __init__(self, canvas):
        self.state = BoardState()

        self.canvas = canvas
        self.spell = True   #if player is allowed to spell
        self.click = True   #for detecting clicks; communicates from events
        self.start_game = False
        self.pool = ""

        self.player = Player(self)
        self.ai = AI(self)

        self.round = 1

        self.turn = True #True = Player; False = AI
        self.mode = True #True = CB; False = MM
        
        self.letter_pool = pg.sprite.Group()
        self.letter_used = pg.sprite.Group()
        self.word_guessed = pg.sprite.Group()

    #for each round
    def update_pool(self, pool = None):
        if len(pool) != 10:
            return
        self.pool = pool
        self.letter_pool.empty()
        self.letter_used.empty()
        self.word_guessed.empty()
        self.state.reset()

        for i in range(10):
            self.state.pool[i] = self.pool[i]
            letter = Letter(self.state.pool[i])
            letter.rect.x = i*tilesize.x
            self.letter_pool.add(letter)

    #for each turn
    def reset_pool(self):
        self.word_guessed.add(self.letter_used)
        self.letter_pool.empty()
        self.letter_used.empty()

        for i in range(10):
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

        if self.turn and self.mode:
            self.player.codebreaker()
        elif self.turn and self.mode:
            self.player.mastermind()
        elif self.turn and self.mode:
            self.ai.codebreaker()
        elif self.turn and self.mode:
            self.ai.mastermind()


        #TEMPORARY FEEDBACK
        letter : Letter
        if self.state.verify_guess():
            for letter in self.letter_used:
                letter.fill = GREEN
                letter.draw()
        else:
            for letter in self.letter_used:
                letter.fill = RED
                letter.draw()
        
        for letter in self.letter_pool:
            if letter not in self.letter_used:
                letter.fill = WHITE
                letter.draw()

        self.update()

    def guess(self): #This is attached to the button in wordwiz.py as a callback
        if self.state.accept_guess():
            self.reset_pool()

    def draw_board(self):
        ...

    def update(self):
        if self.state.win:
            print("Congratulations")
            self.state.win = False
            self.update_pool(self.pool)

    def start(self):
        #set role of player
        ...
    
    def restart(self):
        #end of game condition
        ...

    def events(self, event):
        ...