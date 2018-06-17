# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:35:24 2018

@author: yinjiang
"""

import math, collections

class LaplaceTrigramLM(object):
    
    def __init__(self, corpus):
        
        """
        Trigram Languange Model with add-one smoothing is implemented.
        """
        
        self.total = 0
        self.LaplaceTrigramCount = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: 0)))
        self.LaplaceBigramCount = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
        self.LaplaceUnigramCount = collections.defaultdict(lambda: 0)
        self.train(corpus)
    
    def train(self, corpus):
        """
        Takes a corpus and trains your language model
        Compute any counts or other corpus statistics in this function
        """
        lasttoken1 = '&'
        lasttoken2 = '#'
        for sentence in corpus.corpus:
            for datum in sentence.data:
                token = datum.word
                self.LaplaceUnigramCount[token]=self.LaplaceUnigramCount[token]+1
                self.LaplaceBigramCount[lasttoken1][token]=self.LaplaceBigramCount[lasttoken1][token]+1
                self.LaplaceTrigramCount[lasttoken2][lasttoken1][token]=self.LaplaceTrigramCount[lasttoken2][lasttoken1][token]+1
                self.total += 1
                lasttoken2 = lasttoken1
                lasttoken1 = token
                
    def score(self, sentence):
        """
        Takes a list of strings and returns the log-probability of the sentence
        using the language model.
        """
        score = 0.0
        additional = len(self.LaplaceUnigramCount.items())
        lasttoken1 = '&'
        lasttoken2 = '#'
        for token in sentence:
            count = self.LaplaceTrigramCount[lasttoken2][lasttoken1][token] + 1
            score = score + math.log(count)-math.log(self.LaplaceBigramCount[lasttoken1][token] + additional)
            lasttoken2 = lasttoken1
            lasttoken1 = token
        return score