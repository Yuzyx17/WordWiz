from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.board import Board

from src.ai.codebreaker import Codebreaker
from src.ai.mastermind import Mastermind

class AI():
    def __init__(self, board: Board):
        self.board = board
        self.state = self.board.state
        self.trie = self.state.trie
        self.agent_codebreaker: Codebreaker = None
        self.agent_mastermind: Mastermind = None
        self.score = 0
    
    def codebreaker(self, pool, hint):
        self.agent_codebreaker = Codebreaker(self.trie, pool, hint)
    
    def mastermind(self, pool):
        self.agent_mastermind = Mastermind(self.trie, pool)
        self.state.word_string = self.agent_mastermind.generateWord()
        self.board.turn = True
        self.board.mode = True
    
    def update_codebreaker(self, hints):
        self.agent_codebreaker.rethink(hints)