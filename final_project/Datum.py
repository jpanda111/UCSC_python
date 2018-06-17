# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 19:47:08 2018

@author: yinjiang
"""
import re

class Datum(object):
    word = '' # the correct word
    error = '' # the error word if any
    
#    def __init__(self):
#        self.word = ''
#        self.error = ''
        
    def __init__(self, word, error=''):
        self.word = word
        self.error = error

    def fixError(self):
        # remove all the errors
        return Datum(self.word, '')
    
    def hasError(self):
        if self.error:
            return True
        else:
            return False
    
    def dameraulevenshtein(self, seq1, seq2):
        """
        Calculate the Damerau-Levenshtein distance between sequences
        This distance is the number of additions, deletions, substituitions and 
        transpositions needed to transform seq1 into seq2.
        O(N*M) time and O(M) space, for N and M the lengths of seq1 and seq2.
        >>> dameraulevenshtein('ba', 'abc')
        2
        >>> dameraulevenshtein('fee', 'deed')
        2
        It works with arbitrary sequences too:
        >>> dameraulevenshtein('abcd', ['b', 'a', 'c', 'd', 'e'])
        2
        """
        oneago = None
        thisrow = list(range(1, len(seq2)+1))+[0]
        for x in range(len(seq1)):
            # Python lists wrap around for negative indices, so put the
            # leftmost column at the *end* of the list. This matches with
            # the zero-indexed strings and saves extra calculation.
            twoago, oneago, thisrow = oneago, thisrow, [0]*len(seq2)+[x+1]
            for y in range(len(seq2)):
                delcost = oneago[y]+1
                addcost = thisrow[y-1]+1
                subcost = oneago[y-1] + (seq1[x] != seq2[y])
                thisrow[y] = min(delcost, addcost, subcost)
                # this deals with transpositions
                if (x>0 and y>0 and seq1[x]==seq2[y-1] and seq1[x-1]==seq2[y] and seq1[x] != seq2[y]):
                    thisrow[y] = min(thisrow[y], twoago[y-2]+1)
        return thisrow[len(seq2)-1]
    
    def isValidTest(self):
        """
        Returns true if the error is within edit distance and contains no numerics/punctuation.
        """
        if not self.hasError():
            return False
        distance = self.dameraulevenshtein(self.word, self.error)
        if (distance > 1):
            return False
        # make sure it do not contain numerics/punctuation, otherwise it's false
        regex = ".*[^a-zA-z].*"
        if re.match(regex, self.word) or re.match(regex, self.error):
            return False
        return True
    
    def __str__(self):
        """
        Format: word(error)
        """
        rep = self.word
        if self.hasError():
            rep = rep+" (" + self.error+ ")"
        return rep