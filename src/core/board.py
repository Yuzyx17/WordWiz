import pygame as pg

from src.core.state import BoardState
from src.core.letters import Letter
from src.game.player import Player
from src.game.ai import AI
from src.constants import *

class Board():
    def __init__(self, canvas):
        self.state = BoardState()
        self.state.word_string = "hedge"
        self.canvas = canvas
        self.spell = True   #if player is allowed to spell
        self.click = True   #for detecting clicks; communicates from events
        self.start_game = False
        self.pool = ""

        self.player = Player(self)
        self.ai = AI(self)

        self.round = 1

        self.turn = False #True = Player; False = AI
        self.mode = False #True = CB; False = MM
        
        self.letter_pool = pg.sprite.Group()
        self.letter_used = pg.sprite.Group()
        self.word_guessed = pg.sprite.Group()

    #for each round
    def update_turn(self, pool = None):
        if len(pool) != 10:
            return
        self.pool = pool
        self.word_guessed.empty()
        self.letter_pool.empty()
        self.letter_used.empty()
        self.state.reset()

        if not self.turn:
            self.ai.cb_init(self.pool)

        self.state.pool_string = pool
        for i in range(10):
            self.state.pool[i] = self.pool[i]
            letter = Letter(self.state.pool[i])
            letter.rect.x = i*tilesize.x
            self.letter_pool.add(letter)

    def render_hints(self):
        word = self.state.wordify_guess(self.state.attempt-1)
        for index in range(len(word)):
            char = word[index]
            letter = Letter(char)
            letter.rect.topleft = vec2(tilesize.x*index, 100+((self.state.attempt-1)*tilesize.y))
            letter.fill = WHITE
            if self.state.hints[index] == char:
                letter.fill = GREEN
            letter.draw()
            self.word_guessed.add(letter)

    #for each turn
    def reset_pool(self):
        self.render_hints()

        self.letter_pool.empty()
        self.letter_used.empty()

        for i in range(10):
            self.state.pool[i] = self.pool[i]
            letter = Letter(self.state.pool[i])
            letter.rect.x = i*tilesize.x
            self.letter_pool.add(letter)

    def draw(self):
        self.word_guessed.draw(self.canvas)     #drawing guesses
        self.letter_pool.draw(self.canvas)      #drawing pool of letters
        self.letter_used.draw(self.canvas)      #drawing spell attempt

        self.letter_pool.update()
        self.letter_used.update()
        
        #Player Role
        #CB             #MM
        #Phase 1        #Phase 3
                                #Block
        #Phase 2        #Phase 4
                                        #Round
        #Phase 3        #Phase 1
                                #Block
        #Phase 4        #Phase 2

        if not self.turn and not self.mode:             
            self.ai.mastermind(self.pool)                
        elif self.turn and self.mode:                                       
            self.player.codebreaker()           
        elif self.turn and not self.mode:           
            self.player.mastermind()            
        elif not self.turn and self.mode:                                       
            self.ai.codebreaker()               


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

        if self.turn and self.mode:
            if self.state.accept_guess():
                self.reset_pool()
        if not self.turn and self.mode:
            candidate = self.ai.agent_codebreaker.think()
            self.ai.agent_codebreaker.update_candidate()
            self.ai.update_codebreaker(self.state.hints)
        # print(self.word_guessed)
        # print(self.ai.mastermind(self.pool))

    def draw_board(self):
        ...

    def update(self):
        self.on_win_as_codebreaker()
        self.on_lose_as_codebreaker()

    def on_win_as_codebreaker(self):
        if self.state.win:
            print("Congratulations")
            self.state.win = False
            self.update_turn(self.pool)
        
    def on_lose_as_codebreaker(self):
        if self.state.get_guess_attempts() == 0:
            print(f'YOU LOSE! word is {self.state.word_string}')
            self.state.reset()
            self.update_turn(self.pool)

    def start(self):
        #set role of player
        ...
    
    def restart(self):
        #end of game condition
        ...

    def events(self, event):
        ...