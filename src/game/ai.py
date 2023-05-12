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
        self.codebreaker: Codebreaker = None
        self.mastermind: Mastermind = None
        self.role = None
        self.score = 0
    
    def codebreaker(self, trie, pool, hint):
        self.codebreaker = Codebreaker(trie, pool, hint)
        self.role = True
    
    def mastermind(self, trie, pool):
        self.mastermind = Mastermind(trie, pool)
        self.role = False

    def generateWord(self):
        if self.role is not None:
            if self.role:
                return self.codebreaker.think()
            elif not self.role:
                return self.mastermind.generateWord()
    
    def update_codebreaker(self, hints):
        self.codebreaker.rethink(hints)