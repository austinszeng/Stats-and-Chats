#
# CSCI 121 Fall 2021
#
# Project 2, Part 2
#
# chats.py
#
# Process a text and distill statistics about the bi-gram and tri-gram
# word occurrences in the entered text. It does this by using a dictionary
# of words and bi-grams. Each dictionary entry gives the list of words
# in the text that follow that word/bi-gram (and possibly a count of the
# number of times each follower does so).
#
# The code then generates random text based on these statistics.
#
#
# Usage: python3 chats.py
#
# This command processes a series of lines of text, looking for
# contiguous runs of alphabetic characters treating them each as a
# word. For each such word, it keeps a count of the number of its
# occurrences in the text.
#
# To end text entry hit RETURN and then CTRL-d.  It then generates
# a random text that tries to mimic the text it just processed.
#
#
# Alternative usage: python3 chats.py < textfile.txt
#
# The above instead processes the text of the file in 'textfile.txt'.
#

import sys
import random

STOPPERS   = [".", "!", "?"]
WHITESPACE = [" ","\n","\r","\t"]

def simplifyWord(word):
    """Returns the given string with only certain chars and lowercase.

    This "simplifies" a word so that it only contains a sequence of
    lower case letters and apostrophes, making uppercase letters
    lowercase, and skipping others.  It returns the "simplified" word.
    If, upon simplifying a word, all the characters are skipped, the 
    function returns None.
    
    In normal use, this would convert a word like "Ain't" into the
    word "ain't" and return it. It also would take a text string like
    "it105%s" and give back the string "its".

    This particular function behavior is somewhat arbitrary, written
    to be "good enough" just to handle the spurious other characters
    that might arise in the kinds of free texts from things like
    Project Gutenberg. Sadly, this also strips out accented characters
    and non-Roman alphabetic characters.
    """

    # Scan the word for a-z or ' characters.
    convertedWord = "";
    for c in word:
        if 'A' <= c and  c <= 'Z':
            c = c.lower()
        if ('a' <= c and c <= 'z') or c == '\'':
            convertedWord += c;

    # If we added any such characters, return that word.
    if len(convertedWord) > 0:
        return convertedWord
    else:
        # Otherwise, return None.
        return None

def readWordsFromInput():
    """Returns the contents of console input as a list of words.

    Process the console input as consisting of lines of words. Return
    a list of all the words along with the strings that are "stoppers." 
    Each non-stopper word in the list will be lowercase consisting only
    of the letters 'a'-'z' and also apostrophe. All other characters are
    stripped from the input. Stopper words are specified by the variable
    STOPPERS.
    """
     
    def spacedAround(text,c):
        """Returns modified text with spaces around any occurrence of c.

        Helper function that replaces any string `text` that has the
        character `c` so that all the occurrences of `c` are replaced
        with the substring " c ".
        """
        
        splits = text.split(c)
        return (" "+c+" ").join(splits)

    def spaceInsteadOf(text,c):
        """Returns modified text with space replacing any c.

        Helper function that replaces any string `text` that has the
        character `c` so that all the occurrences of `c` are replaced
        with a space.
        """
        
        splits = text.split(c)
        return (" ").join(splits)
    
    # Read the text into one (big) string.
    textChars = sys.stdin.read()

    # Add spaces around each "stopper" character.
    for stopper in STOPPERS: 
        textChars = spacedAround(textChars,stopper)
        
    # Replace each whitespace character with a space.
    for character in WHITESPACE: 
        textChars = spaceInsteadOf(textChars,character)

    # Split the text according to whitespace.
    rawWords = textChars.split(" ")

    # Process the raw words, simplifying them in the process by
    # skipping any characters that we don't currently handle.
    # We treat the "end of sentence"/"stopper" words specially,
    # including them in the list as their own strings.
    words = []
    for word in rawWords:
        if word not in STOPPERS:
            word = simplifyWord(word)
        if word is not None:
            words.append(word)
    return words


def train(theWords):
    """ Takes a list of words and stoppers and returns a dictionary whose
    keys are either single words or bigrams. 
    
    Each entry represents all possible bigrams that start with that single 
    word or all possible trigrams that start with that bigram. The data 
    associated with each key in the dictionary should be that word's/
    bigram's list of follower words. In a bigram key, the string is two 
    words separated by a space.
    
    We consider stopper punctuation marks as keys or as parts of a bigram.
    The first word in the text should be considered a follower of all the
    stoppers. If the last word in the list is not a stopper, then it should
    have an entry with "." as one of its followers."""

    biTriDict = {}

    # first word is follower of all stoppers
    for s in STOPPERS:
        if s not in biTriDict:
            biTriDict[s] = [theWords[0]]
        else:
            biTriDict[s].append(theWords[0])

    # for bigrams
    s = 0
    while s < len(theWords) - 1:
        if theWords[s] not in biTriDict:
            biTriDict[theWords[s]] = [theWords[s + 1]]
        else:
            biTriDict[theWords[s]].append(theWords[s + 1])
        s += 1

    # for trigrams
    s = 0 
    while s < len(theWords) - 2:
        if theWords[s + 1] != ".":
            bi = theWords[s] + ' ' + theWords[s + 1]
            if bi not in biTriDict:
                biTriDict[bi] = [theWords[s + 2]]
            else:
                biTriDict[bi].append(theWords[s + 2])
        s += 1

    return biTriDict


def chat(biTriDict,numLines,lineWidth):
    """ Start a random chat by picking a random follower from the word
    entry for ".", then pick a follower from the bigram entry for "." and
    that word. Generating the next words continues in this way, by keeping
    track of the last two words that were generated.
    
    1. If the last two words are w1 and w2 (where either could be a stopper),
    pick a random follower from the list associated with that bigram.
    
    2. If there is no entry for that bigram, or only one word was generated so
    far, pick a random follower from the list associated with the last word
    that was just generated.
    
    3. If there is no entry for the last word, or if no words have been 
    generated yet, pick a random follower from the list associated with the
    stopper ".".
    
    If the total number of characters (including spaces) generated on the 
    current line of text of the chat has just exceeded lineWidth, then
    create a new line. If we generate a stopper and the total number of 
    lines with output so far with the chat has exceeded numLines, stop
    the chat generation process."""

    string = ""
    charCount = 0
    lineCount = 1
    lastTwo = ["."]
    allKeys = biTriDict.keys()
    running = True
    while running:
        # to account for instances such as "blah ." that are not key values in the biTriDict (avoid key error)
        if lastTwo[len(lastTwo)-1] in STOPPERS:
            r1 = random.choice(biTriDict[lastTwo[len(lastTwo)-1]])
            string += r1 + " "
            charCount += len(r1) + 1
            lastTwo.append(r1)
        # if last 2 words (bigram) not a key in the dictionary or only one follower, pick a random follower from 
        # the last word generated
        elif lastTwo[len(lastTwo)-2] + " " + lastTwo[len(lastTwo)-1] not in allKeys\
             or len(biTriDict[lastTwo[len(lastTwo)-2] + " " + lastTwo[len(lastTwo)-1]]) <= 1:
            r1 = random.choice(biTriDict[lastTwo[len(lastTwo)-1]])
            if r1 in STOPPERS:
                # remove new line so line doesn't start with a stopper
                if charCount == 0:
                    string = string.rstrip()
                # remove space before period
                else:
                    string = string.rstrip(" ")
                    charCount -= 1
            # re-add the new line after adding the stopper
            if r1 in STOPPERS and charCount == 0:
                string += r1 + "\n"
                charCount += len(r1) 
            else:
                string += r1 + " "
                charCount += len(r1) + 1
            lastTwo.append(r1)

        # pick a random follower from bigram entry for last two words
        elif len(biTriDict[lastTwo[len(lastTwo)-2] + " " + lastTwo[len(lastTwo)-1]]) > 1:
            r1 = random.choice(biTriDict[lastTwo[len(lastTwo)-2] + " " + lastTwo[len(lastTwo)-1]])
            if r1 in STOPPERS:
                # remove new line so line doesn't start with a stopper
                if charCount == 0:
                    string = string.rstrip()
                # remove space before period
                else:
                    string = string.rstrip(" ")
                    charCount -= 1
            # re-add the new line after adding the stopper
            if r1 in STOPPERS and charCount == 0:
                string += r1 + "\n"
                charCount += len(r1)
            else:
                string += r1 + " "
                charCount += len(r1) + 1
            lastTwo.append(r1)

        # create new line when characters on current line exceed lineWidth
        if charCount >= lineWidth:
            string += "\n"
            lineCount += 1
            charCount = 0

        # if a stopper is generated when the number of line >= numLines, stop the chat generation process
        if r1 in STOPPERS and lineCount >= numLines:
            running = False
    
    print(string)


#
# The main script. This script does the following:
#
# * Processes a series of lines of text input into the console.
#      => The words of the text are put in the list `textWords`
#
# * Scans the text to compute statistics about bi-grams and tri-
# grams that occur in the text. This uses the function `train`.
#
# • Generates a random text from the bi-/tri-gram dictionary
#   using a stochastic process. This uses the procedure 'chat'.
#

if __name__ == "__main__":

    # Read the words of a text (including ".", "!", and "?") into a list.
    print("READING text from STDIN. Hit ctrl-d when done entering text.")
    textWords = readWordsFromInput()
    print("DONE.")

    # Process the words, computing a dictionary.
    biTriDict = train(textWords)
    chat(biTriDict, 30, 70)
