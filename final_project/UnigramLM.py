# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 21:11:33 2018

@author: yinjiang
"""

import math, collections

class UnigramLM(object):
    
    def __init__(self, corpus):
        
        """
        Unsmoothed Unigram Languange Model is implemented.
        """
        
        self.unigramCounts = collections.defaultdict(lambda:0)
        self.total = 0
        self.train(corpus)
        
    def train(self, corpus):
        """
        Takes a corpus and trains your language model
        Compute any counts or other corpus statistics in this function
        """
        for sentence in corpus.corpus:
            for datum in sentence.data:
                token = datum.word
                self.unigramCounts[token] = self.unigramCounts[token] + 1
                self.total +=1
    
    def score(self, sentence):
        """
        Takes a list of strings and returns the log-probability of the sentence
        using the language model.
        """
        score = 0.0
        for token in sentence:
            count = self.unigramCounts[token]
            if count>0:
                score = score + math.log(count) - math.log(self.total)
            else:
                score = float("-inf") # unseen, not smoothed
        return score