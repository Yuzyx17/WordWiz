from src.ai.codebreaker import Codebreaker
from src.ai.mastermind import Mastermind

class AI():
    def __init__(self):
        self.codebreaker = None
        self.mastermind = None
        self.role = None
    
    def as_codebreaker(self, trie, pool, hint):
        self.codebreaker = Codebreaker(trie, pool, hint)
        self.role = True
    
    def as_mastermind(self, trie, pool):
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