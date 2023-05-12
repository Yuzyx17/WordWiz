from src.constants import *
from src.ai.codebreaker import Codebreaker
from src.ai.mastermind import Mastermind
from src.utils.trie import Trie
from timeit import default_timer as timer
from collections import defaultdict

def sampleCB(word = "glass", pool = "gonianless"):
    start = timer()

    trie = Trie()
    trie.save()
    trie.load()

    hints = defaultdict(defaultValue)

    ai = Codebreaker(trie, pool, hints)
    print("\n---STATS---\n")
    for i in range(6):
        
        candidate = ai.think()
        for index in range(len(candidate)):
            if word[index] == candidate[index]:
                hints[index] = word[index]
        
        ai.attempts[candidate] = ai.candidates[candidate]
        ai.stats()
        ai.rethink(hints)

        if candidate == word:
            print("------------------------------------")
            print(f'ANWSER: {candidate} | ATTEMPTS:{i+1}')
            print("------------------------------------")
            break    
        elif i == 5:
            print("------------------------------------")
            print(f'NO ANWSER')
            print("------------------------------------")

    end = timer()
    print('finish at:', str(end - start))


def sampleMM(pool="jzkjsdausz"):
    trie = Trie()
    trie.save()
    trie.load()
    ai = Mastermind(trie, pool)
    print(ai.generateWord())