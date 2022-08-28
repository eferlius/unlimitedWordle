# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 08:23:52 2022

@author: eferlius
"""

import random
import string
import matplotlib.pyplot as plt
import os

def loadList(filename):
    return open(filename).read().splitlines()

def replaceCharAtIndex(s, position, character):
    return s[:position] + character + s[position+1:]

def compareWords(cw, tw):
    '''
    Compares two words of 5 letters, outputs a string of:
        - x: the letter in try word is not present in correct word
        - ?: the letter in try word is present in correct word but in another position
        - !: the letter in try word is present in correct word in the same position


    Parameters
    ----------
    cw : string
        correct word.
    tw : string
        try word.

    Returns
    -------
    stringResult : string
        contains x?! to indicate the correctness of each letter.

    '''
    listResult = list('xxxxx')

    cwcopy = cw
    twcopy = tw
    # check green letters (same letter in correct position)
    for i in range(5):
        if cw[i] == tw[i]:
            listResult[i] = '!'
            # to be sure they're different
            twcopy = replaceCharAtIndex(twcopy, i, '_')
            cwcopy = replaceCharAtIndex(cwcopy, i, '^')
    # check yellow letters (same letter in wrong position)
    for i in range(5):
        if listResult[i] != '!': # if not already checked letter
            if twcopy[i] in cwcopy:
                listResult[i] = '?'
                cwcopy = replaceCharAtIndex(cwcopy, cwcopy.index(twcopy[i]), '*')
                twcopy = replaceCharAtIndex(twcopy, i,'*')

    stringResult = "".join(listResult)

    return stringResult

def lettersNotInWord(tw, cw):
    '''
    Compares try word and correct word, outputs a list containing all the letters in try word not contained in correct word
    

    Parameters
    ----------
    cw : string
        correct word.
    tw : string
        try word.

    Returns
    -------
    notPresentLetters : list
        containing all the letters in try word not contained in correct word.

    '''
    notPresentLetters = []
    for l in tw:
        if l not in cw:
            notPresentLetters.append(l)
    return notPresentLetters

def askQuestion(question, listOfPossibleAnswers, caseSensitive = False, showOptions = True, answerInArray = False):
    '''
    Ask a question with the possible answers, outputs the integer corresponding to the given answer

    Parameters
    ----------
    question : string
        DESCRIPTION.
    listOfPossibleAnswers : list
        DESCRIPTION.
    caseSensitive : bool, optional
        DESCRIPTION. The default is False.
    showOptions : bool, optional
        DESCRIPTION. The default is True.
    answerInArray : bool, optional
        If True, if the user's answer is not in the possible list, asks again the question.
        If False, if the user's answer is not in the possible list, outputs -1. 
        The default is False.

    Returns
    -------
    idx : int
        corresponds to the answer in the list.

    '''
    idx = len(listOfPossibleAnswers)+1
    while idx > len(listOfPossibleAnswers):
        answer = input(question + '\nopt: '+str(listOfPossibleAnswers)+': ')
        if not caseSensitive: # put everything in lowercase
            listOfPossibleAnswers = [x.lower() for x in listOfPossibleAnswers]
            answer = answer.lower()
        try:
            idx = listOfPossibleAnswers.index(answer)
        except:
            if answerInArray:
                print('not valid answer')
                len(listOfPossibleAnswers)+1
            if not answerInArray:
                idx = -1


    return idx

def askQuestionYN(question, answerInArray = False):
    answer = askQuestion(question, ['y','n'], caseSensitive = False, showOptions = True, answerInArray = answerInArray)
    if answer == 0:
        return True
    else:
        return False



POSSIBLE_WORDS_PATH = r'valid-wordle-words.txt'
SAVE_IMAGES_PATH = r'playedGames'


os.makedirs(SAVE_IMAGES_PATH, exist_ok = True)
# load the possible words
possibleWords = loadList(POSSIBLE_WORDS_PATH)

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
    ax[0].set_title(correctWord)

    plt.pause(0.01)
    plt.show()
    plt.draw()

    if tryWord != correctWord:
        attemptCounter = 'X'

    save = askQuestionYN('Save figure?')
    if save:
        plt.savefig(os.path.join(SAVE_IMAGES_PATH,correctWord+str(attemptCounter)+'.png'))


    play = askQuestionYN('Play again?')
    if play:
        # clear all the axes
        for i in range(6):
            ax[i].clear()

        plt.pause(0.01)
        plt.show()
        plt.draw()
