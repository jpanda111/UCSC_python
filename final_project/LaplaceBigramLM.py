# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:04:42 2018

@author: yinjiang
"""

import math, collections

class LaplaceBigramLM(object):
    
    def __init__(self, corpus):
        
        """
        Bigram Languange Model with add-one smoothing is implemented.
        """
        
        self.total = 0
        # set default value to be 0, the first arg must be callable, so you cannot do 0 directly but use lambda
        # for bigram, you do dict of dict to store last token and current token
        self.LaplaceBigramCount = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
        self.LaplaceUnigramCount = collections.defaultdict(lambda: 0) 
        self.train(corpus)
        
    def train(self, corpus):
        """
        Takes a corpus and trains your language model
        Compute any counts or other corpus statistics in this function
        """
        lasttoken = '&'
        for sentence in corpus.corpus:
            for datum in sentence.data:
                token = datum.word
                self.LaplaceUnigramCount[token]=self.LaplaceUnigramCount[token]+1
                self.LaplaceBigramCount[lasttoken][token]=self.LaplaceBigramCount[lasttoken][token]+1
                lasttoken = token
                self.total += 1
    
    def score(self, sentence):
        """
        Takes a list of strings and returns the log-probability of the sentence
        using the language model.
        In Laplace Bigram language model, add-one smoothing technique applied for unseen words
        """
        score = 0.0
        lasttoken = '&'
        additional = len(self.LaplaceUnigramCount.items())
        for token in sentence:
            count = self.LaplaceBigramCount[lasttoken][token]+1 # Add-one smoothing for unseen words
            score = score + math.log(count) - math.log(self.LaplaceUnigramCount[token]+additional)
            lasttoken = token
        return score