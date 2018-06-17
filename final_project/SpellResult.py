# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 19:06:05 2018

@author: yinjiang
"""

class SpellResult(object):
    """
    Calculate accuracy of a given language model
    """
    numCorrect = 0
    numTotal = 0
    
    def __init__(self, correct, total):
        self.numCorrect= correct
        self.numTotal=total
    
    def getAccuracy(self):
        if self.numTotal==0:
            return 0.0
        else:
            return float(self.numCorrect)/self.numTotal
    
    def __str__(self):
        return "language model correct: %d total %d accuracy %f " %(self.numCorrect, self.numTotal, self.getAccuracy())
