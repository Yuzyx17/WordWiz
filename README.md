# WORDWIZ

This game is insprired of both wordle and codebreaker. We combined the general idea of both games to create WordWiz
In this game

![alt text](assets\img\1.png)

You can either play as a codebreaker or a mastermind

## Instructions

* You will be fighting against an AI in a turn based battle acting as both the codebreaker and mastermind each round.
* You have to type your guess as a codebreaker and have five tries for it, dont worry! the letters will be kept if it was in the correct position similar to Wordle. You can use the backspace to undo a guess letter
* As a mastermind, you need to give the AI a hard word so that he wont be able to guess it!

#### Codebreaker

1. You have to guess the word within five tries
2. Each time you make a guess, the correct letters will be saved

![alt text](assets\img\3.png)
![alt text](assets\img\4.png)

#### Mastermind

1. Give the Enemy a hard word and watch him guess it.

![alt text](assets\img\5.png)

### This project is made for our Artificial Intelligence class

This game was made as an entry for our project in our AI class. The AI develop here is a word guesser AI

It uses a trie structure to store all the possible words in a dictionary, since the word are only five letter long, this is easily one of the best option to store the dictionary.

![alt text](assets\img\7.png)

Another benefit of trie is it's ability to cater our chosen AI algorithm, the very simple **Depth First Search**. It works by continously searching the tree, it is quite simple as the trie already terminates branches that does not contain any letters that would create a word.

All it have to do is search for an initial word and from that a hint may or may not appear, if it doesnt appear it just have to randomly select another starting letter and get the first word it will generate, similar to how we would normally do it as humans. 

If it finds a hint it will then use that as a context and anchor skipping all other letters from that depth of the branch.

# TL;DR

This project combines both Wordle and Codebreaker. The player and AI plays the role of both codebreaker and mastermind each round. The AI uses the combination of Trie and DFS to generate and guess a word.

----

 This was a very fun project to made and it challenged me to become more innovative and creative when creating solutions. Using simple algorithms to create simple yet mildly-complex game