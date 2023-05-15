from src.utils.trie import Trie, TrieNode
from src.constants import defaultValue, getLetterIndex
from collections import defaultdict, Counter
import random as rd

class Mastermind():
    def __init__(self, node: Trie, pool: str = "abcdefghijklmnopqrstuvwxyz") -> None:
        self.node = node
        self.pool = [letter for letter in pool]
        self.pool_stack = []
        self.candidates = defaultdict(defaultValue)
        self.max_candidates = 500
        self.globalScore = 0
        self.word = []

    def generateWord(self):
        self.search(self.node.nodes, 0)
        for word in self.candidates.keys():
            self.candidates[word] += rd.randint(1, 5) * rd.randint(-3, 3)
            # stats = Counter(word)
            # for values in stats.values():
            #     self.candidates[word] *= values
        
        # print(dict(sorted(self.candidates.items(), key=lambda x:x[1])))
        if len(self.candidates) != 0:
            # return min(self.candidates, key=self.candidates.get)
            # return max(self.candidates, key=self.candidates.get)
            middle = len(self.candidates)//2
            return list(self.candidates.keys())[middle]
            return 
        return ""
    
    def convertWord(self):
        word = ""
        for letter in self.word: word += letter
        return word
    
    def search(self, node: TrieNode, depth):
        if depth >= 5:
            return
        for letter in rd.sample(self.pool, len(self.pool)):
            if len(self.candidates) == self.max_candidates:
                return
            self.word.append(letter)     
            current_node = node.nodes[getLetterIndex(letter)]
            self.globalScore += current_node.frequency() if current_node is not None else 0
            if current_node:  
                          
                if self.node.search(self.convertWord()):
                    word = self.convertWord() 
                    if word not in self.candidates:
                        self.candidates[word] = self.globalScore
                # self.pool_stack.append(self.pool.pop(self.pool.index(letter)))
                self.search(current_node, depth+1)
                # self.pool.append(self.pool_stack.pop(self.pool_stack.index(letter)))
            self.globalScore -= current_node.frequency() if current_node is not None else 0
            self.word.pop()
    