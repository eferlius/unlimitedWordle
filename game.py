# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 08:23:52 2022

@author: eferlius
"""

import random
import string
import matplotlib.pyplot as plt
import cv2
import time

def loadList(filename):
    return open(filename).read().splitlines()

def replaceCharAtIndex(s, position, character):
    return s[:position] + character + s[position+1:]

def compareWords(cw, tw):
    # cw = correct word
    # tw = try word
    listResult = list('xxxxx')

    cwcopy = cw
    twcopy = tw

    # check green letters
    for i in range(5):
        if cw[i] == tw[i]:
            listResult[i] = '!'
            # to be sure they're different
            twcopy = replaceCharAtIndex(twcopy, i, '_')
            cwcopy = replaceCharAtIndex(cwcopy, i, '^')
        # print(twcopy)
        # print(cwcopy)
    # check yellow letters in the whole word
    for i in range(5):
        if listResult[i] != '!': # if not already checked letter
            if twcopy[i] in cwcopy:
                listResult[i] = '?'
                cwcopy = replaceCharAtIndex(cwcopy, cwcopy.index(twcopy[i]), '*')
                twcopy = replaceCharAtIndex(twcopy, i,'*')

        # print(twcopy)
        # print(cwcopy)

    stringResult = "".join(listResult)

    return stringResult

def lettersNotInWord(tw, cw):
    notPresentLetters = []
    for l in tw:
        if l not in cw:
            notPresentLetters.append(l)
    return notPresentLetters





# load the possible words
possibleWordsPath = r'valid-wordle-words.txt'
possibleWords = loadList(possibleWordsPath)

plt.close('all')
fig, ax = plt.subplots(6,1)
plt.ion()
plt.suptitle('unlimited wordle')


play = True
while play == True:
    print('\n','WORDLE GAME')

    # load the possible letters (are erased during the attempt)
    alphabet_string = string.ascii_lowercase
    possibleLetters = list(alphabet_string)


    # chose a random word
    correctWord = random.choice(possibleWords)
    # correctWord = input('insert the word to be guessed: ')
    # print(correctWord) # comment this
    
    tryWord = '00000'
    

    attemptCounter = 0
    while tryWord != correctWord and attemptCounter < 6:
        print(possibleLetters)
        attemptCounter += 1
        tryWord = '00000'

        while tryWord not in possibleWords:
            tryWord = input('write your guess: ')

        lettersToEliminate = lettersNotInWord(tryWord, correctWord)


        for l in lettersToEliminate:
            try:
                possibleLetters.remove(l)
            except:
                pass
                # do nothing, it means the letter was already removed

        stringResult = compareWords(correctWord, tryWord)

        print(str(attemptCounter) + ': ' + tryWord)
        print(str(attemptCounter) + ': ' + stringResult)
    
        for i in range(5):
            letterResult = stringResult[i]
            if letterResult == 'x':
                col = 'k'
            elif letterResult == '?':
                col = 'y'
            elif letterResult == '!':
                col = 'g'
            ax[attemptCounter-1].annotate(tryWord[i],(0+i*0.2,0), fontsize = 50, color = col)
    
        plt.pause(0.01)
        plt.show()
        plt.draw()
    print(correctWord)

    answer = input('Play again? [y/n] ')
    if answer.lower() == 'y':
        play = True
        # clear all the eaxes
        for i in range(6):
            ax[i].clear()

        plt.pause(0.01)
        plt.show()
        plt.draw()
    else:
        play = False
