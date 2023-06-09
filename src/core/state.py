from typing import List
from collections import defaultdict

from src.constants import *
from src.utils.trie import Trie

#############################################################
# self.ai.score        self.code        self.player.score   #
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
        self.trie = Trie()
        self.hints = defaultdict(defaultValue)

        self.pool = dict(zip((i for i in range(10)), (' ' for _ in range(10)))) #Holds the pool with respective index, index is used for transitions
        self.code: List[dict | str] = [' ' for _ in range(5)]    #Holds the words to be guessed with index from pool for transition
        self.guesses: List[List[dict | str]] = []  #Holds the guess with index from pool, this is used for reverting
        self.attempts = []

        self.attempt = 0 #row
        self.index = 0 #col
        
        self.pool_string = ""
        self.code_string = ""

        self.win = False
        
        for _ in range(6):
            guess = []
            for i in range(5):
                guess.append(' ')
            self.guesses.append(guess)

        self.trie.save()
        self.trie.load()

    def reset(self):
        self.hints = defaultdict(defaultValue)

        self.pool = dict(zip((i for i in range(10)), (' ' for _ in range(10)))) #Holds the pool with respective index, index is used for transitions
        self.code: List[dict | str] = [' ' for _ in range(5)]    #Holds the words to be guessed with index from pool for transition
        self.guesses: List[List[dict | str]] = []  #Holds the guess with index from pool, this is used for reverting
        self.attempts = []

        self.attempt = 0 #row
        self.index = 0 #col
        
        self.pool_string = ""
        self.code_string = ""

        self.win = False
        
        for _ in range(6):
            guess = []
            for i in range(5):
                guess.append(' ')
            self.guesses.append(guess)

    def verify_code(self):
        return self.trie.search(self.wordify_code())

    def accept_code(self):
        if self.verify_code():
            self.code_string = self.wordify_code()
            return True
        return False

    def wordify_code(self):
        return "".join([list(x.values())[0] if type(x) == dict else '' for x in self.code])

    def undo_code(self, key, val):
        index = self.code.index({key: val})
        self.code[index] = ' '
        self.pool[key] = val
        return index

    def spell_code(self, key, val):
        self.index = self.code.index(' ')
        self.code[self.index] = {key: val}
        self.pool[key] = ' '
        return self.index

    def can_spell_code(self):
        try:
            self.index = self.code.index(' ')
            return True
        except Exception as e:
            return False

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
        if self.attempt > 5:
            return False
        if self.wordify_guess(self.attempt) in self.attempts:
            return False
        return self.trie.search(self.wordify_guess(self.attempt))
    
    def wordify_guess(self, index):
        return "".join([list(x.values())[0] if type(x) == dict else '' for x in self.guesses[index]])

    def accept_guess(self):
        if self.get_guess_attempts() == 0 or self.code_string == "":
            return False
        word_guess = self.wordify_guess(self.attempt)
        if not self.verify_guess(): return False
        if word_guess in self.attempts: return False
        
        self.attempts.append(word_guess)
        for index in range(5):
            if self.code_string[index] == word_guess[index]:
                self.hints[index] = self.code_string[index]

        if word_guess == self.code_string: 
            self.win = True
            self.index = 0
            self.attempt += 1
            return True
        

        self.index = 0
        self.attempt += 1

        return True
    
    def get_guess_attempts(self):
        return 6 - self.attempt