#
# CSCI 121 Fall 2021
#
# Project 2, Part 1
#
# stats.py
#
# Count and report statistics about the number of occurrences of
# words within some entered text.
#
# Usage: python3 stats.py
#
# This program processes a series of lines of text, looking for
# contiguous runs of alphabetic characters treating them each as a
# word. For each such word, it keeps a count of the number of its
# occurrences in the text.
#
# To end text entry hit RETURN and then CTRL-d.  It then reports a
# summary of the words it found, along with their counts.
#
# Alternative usage: python3 stats.py < textfile.txt
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

def wordFrequencies(wordList):
    """Return dictionary of the counts of words in of the given list.

    Given a list of strings that are either words or "stoppers", count
    the number of times each non-stopper word appears. Return a
    dictionary whose entries are the words and their number of
    occurrences.

    Example:
    >>> wf = wordFrequencies(["hello", "there", ".", "hello", "!"])
    >>> wf
    {'hello':2, 'there':1}

    """
    
    freqs = {}

    for s in wordList:
        if s not in STOPPERS:
            if s not in freqs:
                freqs[s] = 1
            else:
                freqs[s] += 1

    return freqs

def wordCount(freqs):
    """Returns the word count and vocabulary size of a text.

    Given a dictionary of words and their frequency of occurrence,
    computed from a text, return the total number of words that occurred
    in the original text (counting repetions of words) along with the 
    number of distinct words that appeared in that text.

    Example:
    >>> wf = wordFrequencies(["hello", "there", ".", "hello", "!"])
    >>> count,vocabSize = wordCount(wf)
    >>> print(count,vocabSize)
    3,2

    NOTE: this function returns a pair. The first component of the
    pair should is the size of the text in # of words. The second
    component of the pair is the # of distinct words.

    """
    word_count = 0
    distinct_words = 0
    for key in freqs:
        word_count += freqs[key]
        distinct_words += 1        
    return word_count, distinct_words

def topWordExcept(freqs,excluded):
    """Gets the most frequent word in a dictionary that's not excluded.

    Find the most frequently occurring word in a text, excluding any
    words that are in the list `excluded`. The text is summarized by a
    word frequency dictionary `freqs`. If there are no words except
    the excluded ones, this function returns the value `None`.

    Example:
    >>> wf = wordFrequencies(["hello", "there", ".", "hello", "!"])
    >>> topWordExcept(wf,[])
    'hello'
    >>> topWordExcept(wf,['hello'])
    'there'
    >>> print(topWordExcept(wf,['hello','there']))
    None

    """

    counter = 0
    top = None
    for key in freqs:
        if key not in excluded and freqs[key] > counter:
            counter = freqs[key]
            top = key
    return top

    
def topWordsByFrequency(freqs,howMany):
    """Return the top occurring words in a text.

    Return a list of the most frequently occurring words in a text.
    The text is summarized by a word frequency dictionary `freqs`.
    The length of the list of the top-occurring words is dictated by
    the value of `howMany`. E.g. if `howMany == 3` then only the three most
    frequently occurring words should be in that list.

    Example:
    >>> wf = wordFrequencies(["hello", "there", ".", "hello", "!"])
    >>> topWordsByFrequeny(wf,1)
    ['hello']
    >>> topWordsByFrequency(wf,2)
    ['hello', 'there']

    The list of words should be in order of the most frequent to the
    least frequent. If there are several ties for what could be the
    top `howMany`-th most-frequent words, this code can choose any
    of those with equal frequency. For example:

    >>> wf = wordFrequencies(["hello", "there", "goodbye", "abe"])
    >>> twbf = topWordsByFrequency(wf,2)

    Then in the above, `twbf` could contain `hello` and `there`,
    or `hello` and `abe`, or `goodbye` and `there`, etc. Any two
    of those four words are the top two most-frequent words.

    """

    # Words in the excluded list account for the most frequently occuring
    # words in the text and allow for the 2nd, 3rd, etc... most frequent word
    # to be found using the topWordExcept() function.
    excluded = []
    while len(excluded) < howMany:
        top = topWordExcept(freqs, excluded)
        excluded.append(top)
    return excluded


def rankedWordReport(ranking,topWordsList,freqs):
    """ Returns a string reporting a ranking of word occurrences.

    When a text has been summarized with the dictionary `freqs`,
    giving the words in it, and their number of occurrences, and
    then that dictionary has been distilled to the most frequently
    occurring words as a list `topWordsList`, ordered from most-
    to least-frequent, then this function returns a string 
    giving the information about a word of rank `ranking`.

    The format of the string should be the ranking, followed by
    a period, followed by a space, followed by the word, followed
    by a colon character, followed by the number of occurrences
    of that word.

    Suppose, for example, that the word "the" is the most frequent
    word in a text, and it occurs 12345 times. Then calling this
    function with `ranking == 1` will return the string

        "1. the:1235"

    This would also mean that
    
        `topWordsList[0] == "the" and freqs["the"] == 1235`
    
    """
    
    s = ''
    if ranking <= len(topWordsList):
        s += str(ranking) + '. ' + topWordsList[ranking - 1] + ':' + str(freqs[topWordsList[ranking - 1]])
    return s


def numWordsWithFrequency(freqDict,freq):
    """ Return how many words occur some number of times in a text.

    Given a word frequence dictionary `freqDict` and a number of 
    occurrences `freq`, this function returns how many words in
    the dictionary have that count of occurrences.
    """
    
    counter = 0
    for key in freqDict:
        if freqDict[key] == freq:
            counter += 1
    return counter


#
# The main script. This script does the following:
# * Processes a series of lines of text input into the console.
#      => The words of the text are put in the list `textWords`
# * Scans the text to compute the frequency of occurrence of each
#   distinct word in the text.
#      => These are put in the dictionary `frequencies`
# * Reports a series of statistics
#    . The total number of words scanned.
#    . The number of distinct words.
#    . The top most frequently occurring words, by rank.
#    . The number of words that occur exactly once.
#
if __name__ == "__main__":

    # Read the words of a text (including ".", "!", and "?") into a list.
    print("READING text from STDIN. Hit ctrl-d when done entering text.")
    textWords = readWordsFromInput()
    print("DONE.")

    # Process the words, computing a dictionary of word frequencies.
    frequencies = wordFrequencies(textWords)

    # Report some basic statistics about the text.
    print("HERE are the word statistics of that text:")
    textLength,distinctWords = wordCount(frequencies)

    print()
    print("That text was " + str(textLength) + " words in length.")
    print()
    print("There are " + str(distinctWords) + " distinct words used in that text.")

    # Report a word frequency analysis.
    #
    sizeOfReport = 1
    if distinctWords > 10:
        sizeOfReport = 10
        if (distinctWords > 100):
            sizeOfReport = 100

    # Sort the words according to frequency, putting the most frequent word
    # into slot 0, the next most frequent word into slot 1, and so forth.
    topWords = topWordsByFrequency(frequencies,sizeOfReport)

    print()
    print("The top " +str(sizeOfReport) + " ranked words (with their frequencies) are:")

    # Give the top most frequent words.
    rank = 1
    report = ""
    while rank < sizeOfReport:
        report += rankedWordReport(rank,topWords,frequencies)
        report += ", "
        rank += 1
    report += rankedWordReport(sizeOfReport,topWords,frequencies)
    print(report)

    # Report the number of words that appear exactly once.
    #
    appearOnce = numWordsWithFrequency(frequencies,1)
    print()
    print("Among its " + str(distinctWords) + " words, " + str(appearOnce) + " of them appear exactly once.")
