from src.utils.trie import Trie, TrieNode
from src.constants import defaultValue, getLetterIndex
from collections import defaultdict
import random as rd

class Codebreaker():
    
    def __init__(self, trie: Trie, pool: str) -> None:
        self.trie = trie
        self.pool = [letter for letter in pool]
        self.hints = defaultdict(defaultValue)
        self.pool_stack = []
        self.candidate = ""
        self.candidates = defaultdict(defaultValue)
        self.globalScore = 0
        self.max_candidates = 25
        self.word = []
        self.attempts = defaultdict(defaultValue)

    def selectCandidate(self):
        if len(self.candidates) != 0:
            return max(self.candidates, key=self.candidates.get)
        return ""

    def localScore(self):
        localScore = 0
        for word in self.attempts:
            for index in range(len(word)):
                if word[index] == self.word[index]:
                    localScore -= 5
        for index in range(len(self.word)):
            if self.hints[index] == self.word[index]:
                    localScore += 15
        return localScore + self.globalScore/2
    
    def getSampleStats(self, node: TrieNode):
        for letter in self.pool:
            if node.nodes[getLetterIndex(letter)]:
                print(f'{letter}: {node.nodes[getLetterIndex(letter)].frequency()} ')
            else:
                print(f'{letter}: {0} ')
        print()

    def search(self, node: TrieNode = None, depth=0):
        # self.getSampleStats(node)
        used = False
        if depth >= 5:
            return
        for letter in rd.sample(self.pool, len(self.pool)):
            if self.hints[depth]:
                if letter != self.hints[depth]:
                    continue 
            if len(self.candidates) == self.max_candidates:
                return
            
            # for word in self.attempts:
            #     if word and self.hints[depth]:
            #         if word[depth] == letter and self.hints[depth] != word[depth]:
            #             used = True
            #     else:
            #         if word:
            #             if word[depth] == letter:
            #                 used = True
            # if used:
            #     used = False
            #     continue

            self.word.append(letter)     
            current_node = node.nodes[getLetterIndex(letter)]
            self.globalScore += current_node.frequency() if current_node is not None else 0
            if current_node:  
                          
                if self.trie.search(self.convertWord()):
                    word = self.convertWord() 
                    if word not in self.candidates and word not in self.attempts:
                        self.candidates[word] = self.localScore()
                self.pool_stack.append(self.pool.pop(self.pool.index(letter)))
                self.search(current_node, depth+1)
                self.pool.append(self.pool_stack.pop(self.pool_stack.index(letter)))
            self.globalScore -= current_node.frequency() if current_node is not None else 0
            self.word.pop()
            
    
    def stats(self):
        print(self)

    def think(self):
        self.search(self.trie.nodes)
        self.candidate = self.selectCandidate()
        return self.candidate

    def update_candidate(self):
        self.attempts[self.candidate] = self.candidates[self.candidate]

    def rethink(self, hints = None):
        if hints is not None:
            self.hints = hints
        self.candidates = defaultdict(defaultValue)
        
    def convertWord(self):
        word = ""
        for letter in self.word: word += letter
        return word

    def __repr__(self) -> str:
        return (f'candidate: {self.selectCandidate()}\n'+
                f'candidates: {[candidate for candidate in self.candidates.items()]}\n' +
                f'attempts: {[attempt for attempt in self.attempts.items()]}\n' +
                f'hints: {"".join(["_" if self.hints[i] is None else self.hints[i] for i in range(5)])}\n')
