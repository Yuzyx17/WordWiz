import pygame as pg

from src.core.state import BoardState
from src.core.letters import Letter
from src.game.player import Player
from src.game.ai import AI
from src.constants import *

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