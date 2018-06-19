# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:42:41 2018

@author: yinjiang
"""

import math, collections

class StupidBackoffLM(object):
    
    def __init__(self, corpus):
        
        """
        Stupid Backoff Trigram Languange Model is implemented.
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
        lasttoken2 = '#'
        lasttoken1 = '&'
        
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
        In stupid backoff, no smoothing techniques applied, lambda = 0.4
        """
        score = 0.0
        lasttoken2 = '#'
        lasttoken1 = '$'
        for token in sentence:
            triCount = self.LaplaceTrigramCount[lasttoken2][lasttoken1][token]
            biCount = self.LaplaceBigramCount[lasttoken1][token]
            uniCount = self.LaplaceUnigramCount[token]
            if triCount > 0:
                score = score + math.log(triCount) - math.log(self.LaplaceBigramCount[lasttoken2][lasttoken1])
            elif biCount > 0:
                score = score + math.log(0.4) + math.log(biCount) - math.log(self.LaplaceUnigramCount[lasttoken1])
            elif uniCount > 0:
                score = score + math.log(0.4*0.4) + math.log(uniCount) - math.log(self.total)
            else:
                score = score + math.log(0.4*0.4*0.4) - math.log(self.total)
            lasttoken2 = lasttoken1
            lasttoken1 = token
        return score