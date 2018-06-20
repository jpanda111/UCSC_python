# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:42:41 2018

@author: yinjiang
"""

import math, collections

class StupidBackoffSmoothLM(object):
    
    def __init__(self, corpus):
        
        """
        Stupid Backoff Bigram Languange Model is implemented.
        """

        self.total = 0
        self.additional = 0
        self.LaplaceBigramCount = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
        self.LaplaceUnigramCount = collections.defaultdict(lambda: 0)
        self.train(corpus)
    
    def train(self, corpus):
        """
        Takes a corpus and trains your language model
        Compute any counts or other corpus statistics in this function
        """
        lasttoken = '<s>'
        
        for sentence in corpus.corpus:
            for datum in sentence.data:
                token = datum.word
                self.LaplaceUnigramCount[token]=self.LaplaceUnigramCount[token]+1
                self.LaplaceBigramCount[lasttoken][token]=self.LaplaceBigramCount[lasttoken][token]+1
                self.total += 1
                lasttoken = token
    
    def score(self, sentence):
        """
        Takes a list of strings and returns the log-probability of the sentence
        using the language model.
        In stupid backoff, add-one smoothing techniques applied in unigram, lambda = 0.4
        """
        score = 0.0
        lasttoken = '<s>'
        self.additional = len(list(self.LaplaceUnigramCount.items()))
        for token in sentence:
            biCount = self.LaplaceBigramCount[lasttoken][token]
            uniCount = self.LaplaceUnigramCount[token]
            if biCount > 0:
                score = score + math.log(biCount) - math.log(self.LaplaceUnigramCount[lasttoken])
            elif uniCount > 0:
                score = score + math.log(0.4) + math.log(uniCount+1) - math.log(self.total+self.additional)
            else:
                score = score + math.log(0.4*0.4) - math.log(self.total)
            lasttoken = token
        return score