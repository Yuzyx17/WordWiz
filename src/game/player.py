from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.board import Board

from src.core.letters import Letter
from src.constants import *

class Player():
    def __init__(self, board: Board):
        self.board = board
        self.state = self.board.state
        self.role = None
        self.score = 0
    
    def codebreaker(self):
        #TRIAL ONLY FOR WHEN TURN = PLAYER and MODE = CODEBREAKER
        self.board.spell = self.state.can_spell_guess()  #if current board state allows for spelling
        
        letter: Letter
        for letter in self.board.letter_pool:         #for letters in the pool
            if not letter.clicked and letter not in self.board.letter_used:
                if letter.click(self.board.spell and self.board.click):
                    #State update
                    #Gets the index of the letter clicked from pool
                    attempted_index = self.board.letter_pool.sprites().index(letter)        
                    #Gets the FIRST empty slot from self.state.guesses[self.attempt]
                    attempted_index = self.state.spell_guess(attempted_index, letter.letter)
                    #Translate the position of the letter to the empty slot
                    letter.translate(vec2(tilesize.x*attempted_index, 100+(self.state.attempt*tilesize.y)))
                    self.board.letter_used.add(letter)   
                    self.board.click = False
                    break

        for letter in self.board.letter_used:         #for letters used
            if not letter.clicked:
                if letter.click(self.board.click):
                    #State update
                    attempted_index = self.board.letter_pool.sprites().index(letter)
                    letter.translate(vec2(tilesize.x*attempted_index, 25))
                    self.state.undo_guess(attempted_index, letter.letter)
                    self.board.letter_used.remove(letter) 
                    self.board.click = False
                    break
    
    def mastermind(self):
        ...