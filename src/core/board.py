import pygame as pg

from src.core.state import BoardState
from src.core.letters import Letter
from src.game.player import Player
from src.game.ai import AI
from src.constants import *

class Board():
    def __init__(self, canvas):
        self.state = BoardState()
        self.state.code_string = "hedge"
        self.canvas = canvas
        self.spell = False   #if player is allowed to spell
        self.click = False   #for detecting clicks; communicates from events
        self.cont = False
        self.start_game = False
        self.pool = ""

        self.player = Player(self)
        self.ai = AI(self)

        self.time = 0
        self.round = 1
        self.phase = 0

        #MASTERMIND ALWAYS STARTS FIRST
        self.turn = False #True = Player; False = AI
        self.mode = False #True = CB; False = MM #DEFAULT FALSE
         
        self.letter_pool = pg.sprite.Group()
        self.letter_used = pg.sprite.Group()
        self.letter_hints = pg.sprite.Group()
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
        self.letter_hints.empty()

        for i in range(10):
            self.state.pool[i] = self.pool[i]
            letter = Letter(self.state.pool[i])
            letter.rect.x = i*tilesize.x
            self.letter_pool.add(letter)

    def draw(self):
        self.word_guessed.draw(self.canvas)     #drawing guesses
        self.letter_pool.draw(self.canvas)      #drawing pool of letters
        self.letter_used.draw(self.canvas)      #drawing spell attempt
        self.letter_hints.draw(self.canvas)

        self.letter_pool.update()
        self.letter_used.update()
        self.letter_hints.update()
        
        if self.phase == 4:
            self.phase = 0
            self.round += 1
            print(f'Round: {self.round}')

        if not self.turn and not self.mode:          
            pass            
        elif self.turn and self.mode:                                       
            self.player.codebreaker()           
        elif self.turn and not self.mode:        
            self.player.mastermind()            
        elif not self.turn and self.mode and self.time % self.ai.speed == 0 :    
            self.time = 0                                   
            self.ai.codebreaker()        

        #TEMPORARY FEEDBACK
        letter : Letter
        if self.state.verify_guess() and self.mode:
            for letter in self.letter_used:
                letter.fill = GREEN
                letter.draw()
        elif self.state.verify_code() and not self.mode:
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
        for letter in self.letter_hints:
            letter.fill = GREEN
            letter.draw()

        self.update()
        self.time += 1
        if self.time % 1000 == 0:
            self.time = 0

    def guess(self): #This is attached to the button in wordwiz.py as a callback
        if not self.turn and not self.mode:
            self.update_turn(self.pool)
            self.ai.mastermind(self.pool)
            self.state.code_string = self.ai.agent_mastermind.generateWord()
            self.change_turn(turns.PCB)
            self.phase += 1
            print("Begin! now Player Codebreaker")
        if self.turn and self.mode:
            if self.state.accept_guess():
                self.reset_pool()
        if self.turn and not self.mode:
            if self.state.accept_code():
                self.reset_pool()
                self.change_turn(turns.ACB)
                self.phase += 1
                self.ai.cb_init(self.pool)   
                print("Begin! now AI Codebreaker")
        if not self.turn and self.mode:
            ...

    def draw_board(self):
        ...

    def update(self):
        ...

    def change_turn(self, turn: turns):
        self.get_scores()
        match turn:
            case turns.PCB:
                self.turn = True
                self.mode = True
            case turns.PMM:
                self.turn = True
                self.mode = False
            case turns.ACB:
                self.turn = False
                self.mode = True
            case turns.AMM:
                self.turn = False
                self.mode = False
            case other:
                raise("ERROR AWIT")

    def get_scores(self):
        print(f'Player: {self.player.score}\nAI: {self.ai.score}')

    def start(self):
        #set role of player
        ...
    
    def restart(self):
        #end of game condition
        ...

    def events(self, event):
        ...