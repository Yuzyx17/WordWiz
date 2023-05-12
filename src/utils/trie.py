import pickle
from src.utils.trienode import TrieNode
#Trie
class Trie():
    #assigns the initial alphabet
    def __init__(self):
        self.nodes = TrieNode()

    #insert a word in the Trie
    def insert(self, word):
        node: TrieNode = self.nodes
        nodes = node.nodes
        for letter in word:
            nodeIndex = ord(letter) - ord('a')
            if nodes[nodeIndex] is None:
                nodes[nodeIndex] = TrieNode()
            node = nodes[nodeIndex]
            nodes = node.nodes

        node.isWord = True 

    #search for word in Trie
    def search(self, word):
        node: TrieNode = self.nodes
        nodes = node.nodes
        for letter in word:
            nodeIndex = ord(letter) - ord('a')
            if nodes[nodeIndex] is None:
                nodes[nodeIndex] = TrieNode()
            node = nodes[nodeIndex]
            nodes = node.nodes
            
        return node.isWord
    
    #load values given that the Trie is saved
    def load(self):
        with open(r"assets/data/trie.dat", "rb") as input_file:
            trie:Trie = pickle.load(input_file)
            self.nodes = trie.nodes
            input_file.close()
    
    #save the Trie object into a dat file
    def save(self, path='assets/data/dictionary.txt'):
        valid_words = []
        with open(path) as word_file:
            valid_words = list(word_file.read().split())
            word_file.close()
        for word in valid_words:
            self.insert(word)

        with open(r"assets/data/trie.dat", "wb") as output_file:
            pickle.dump(self, output_file)