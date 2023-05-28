from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.board import Board

from collections import defaultdict
from src.ai.codebreaker import Codebreaker
from src.ai.mastermind import Mastermind

from src.core.letters import Letter
from src.constants import *

class AI():
    def __init__(self, board: Board):
        self.board = board
        self.state = self.board.state
        self.trie = self.state.trie
        self.pool = ""
        self.hints = defaultdict(defaultValue)
        self.agent_codebreaker: Codebreaker = None
        self.agent_mastermind: Mastermind = None
        self.guess = ""
        self.guess_index = 0
        self.score = 0
        self.speed = 15
        self.word = ""

        self.test = 0
    
    def mastermind(self, pool=None):
        if pool is not None:
            self.agent_mastermind = Mastermind(self.trie, pool)
        else:
            self.agent_mastermind = Mastermind(self.trie)

    def cb_init(self, pool):
        self.agent_codebreaker = Codebreaker(self.trie, pool)

    def codebreaker(self):
        
        if self.guess == "":
            self.guess = self.agent_codebreaker.think()
        letter: Letter
        for letter in self.board.letter_pool:         #for letters in the pool
            if self.guess != "":
                if self.guess[self.guess_index] == letter.letter and letter not in self.board.letter_used:
                    attempted_index = self.board.letter_pool.sprites().index(letter)        
                    attempted_index = self.state.spell_guess(attempted_index, letter.letter)
                    letter.emulated_click()
                    # letter.translate(vec2(tilesize.x*attempted_index, 100+(self.state.attempt*tilesize.y)))
                    letter.translate(get_gus_pos(attempted_index, self.state.attempt))
                    self.board.letter_used.add(letter)   
                    self.guess_index += 1
                    break
        
        if self.state.accept_guess():
            self.update_codebreaker(self.state.hints) 

        self.cb_lost()
        self.cb_win()

    def cb_lost(self):
        if self.state.get_guess_attempts() == 0 and not self.state.win:
            # print(f'YOU LOSE! word is {self.state.code_string}')
            self.score += NO_GUESS_PENALTY
            self.board.player.score += NO_GUESS_REWARD
            self.cb_end()

    def cb_win(self):
        if self.state.win:
            # print("Congratulations")
            self.score += WORD_GUESSED_REWARD
            self.score += self.state.get_guess_attempts() * ATTEMPTS_REWARD
            self.board.player.score += WORD_GUESSED_PENALTY
            self.cb_end()

    def cb_end(self):
        # self.board.update_turn(self.board.pool)
        self.board.display_correct_word()
        self.board.change_turn(turns.AMM)
        self.board.player.word = []
        # self.state.reset()
        # print("Begin! now AI Mastermind")
        
    def update_codebreaker(self, hints):
        self.board.reset_pool()
        self.guess = ""
        self.guess_index = 0
        self.agent_codebreaker.update_candidate()
        self.agent_codebreaker.rethink(hints)
        