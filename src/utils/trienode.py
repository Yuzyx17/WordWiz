from typing import List

#Node of Trie
class TrieNode():
    #Initiates the Node with 26 None values representing each letter
    def __init__(self):
        self.nodes:List[TrieNode | None] = [None for _ in range(26)]
        self.isWord = False
    
    #Gets the frequency or how many times this letter had been used in a particular word given its depth in the Trie
    def frequency(self):
        freq = 0
        for i in self.nodes:
            if i is not None:
                freq += 1
        return freq
