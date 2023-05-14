from src.constants import *
from src.utils.trie import Trie, TrieNode

from collections import defaultdict
import random as rd

class LetterGenerator():

    def __init__(self, trie: Trie) -> None:
        # trie to search a word
        self.trie = trie
        # letters in the mastermind word
        self.mmWord = []
        # the final pool of letters
        self.pool_letters = []
        # to check if the set of pool letters can generate 100 words
        self.candidate_words = []
        # dict to return
        self.final_pool_letter = defaultdict(defaultValue)
        
        # for searching
        self.pool_stack = []
        self.word = []

    # get 5 random letters in alpha 
    # search if it can generate 100 words
    # if yes, terminate and return
    # if not, repeat
    
    def letter_generate(self):

        while True:
            self.generate_pool_letters()
            self.search_word(self.trie.nodes)

            if len(self.candidate_words) >= 100:
                self.final_pool_letter['pool']  = self.pool_letters
                self.final_pool_letter['word count'] = len(self.candidate_words)
                self.final_pool_letter['candidate words'] = self.candidate_words
                return self.final_pool_letter

    # get 5 random letters in alpha + mastermind word's letters
    def generate_pool_letters(self):
        self.pool_letters = rd.sample(alpha, 5) + self.mmWord
        return self.pool_letters

    def convert_word(self):
        word = ""
        for letter in self.word: word += letter
        return word

    def search_word(self, node: TrieNode = None, depth=0):
        if depth >= 5:
            return
        # search for a 5 letter word that have this letters
        for letter in rd.sample(self.pool_letters, len(self.pool_letters)):
            self.word.append(letter)
            current_node = node.nodes[getLetterIndex(letter)]
            if current_node:  

                if self.trie.search(self.convert_word()):
                    word = self.convert_word() 
                    if word not in self.candidate_words:
                        self.candidate_words.append(word)
                self.pool_stack.append(self.pool_letters.pop(self.pool_letters.index(letter)))
                self.search_word(current_node, depth+1)
                self.pool_letters.append(self.pool_stack.pop(self.pool_stack.index(letter)))
            self.word.pop()
