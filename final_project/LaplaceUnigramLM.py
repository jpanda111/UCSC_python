# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 21:15:25 2018

@author: yinjiang
"""

import math, collections

class LaplaceUnigramLM(object):
    
    def __init__(self, corpus):
        
        """
        Unigram Languange Model with add-one smoothing is implemented.
        """
        #setdefault is faster and simpler with small data sets and has an advantage with more heterogeneous key sets;
        #defaultdict is faster for larger data sets with more homogenous key sets;
        self.LaplaceUnigramCounts = collections.defaultdict(lambda:0)
        self.total = 0
        self.additional = 0
        self.train(corpus)
        
    def train(self, corpus):
        """
        Takes a corpus and trains your language model
        Compute any counts or other corpus statistics in this function
        """
        for sentence in corpus.corpus:
            for datum in sentence.data:
                token = datum.word
                self.LaplaceUnigramCounts[token] = self.LaplaceUnigramCounts[token] + 1
                self.total += 1
                
    def score(self, sentence):
        """
        Takes a list of strings and returns the log-probability of the sentence
        using the language model.
        In laplace Unigram language model, add-one smoothing technique applied to unseen words.
        """
        # total tokens inside language model = additional counts added when using add-one smoothing
        self.additional = len(list(self.LaplaceUnigramCounts.items()))
        score = 0.0
        for token in sentence:
            # Add-one smoothing for unseen words
            count = self.LaplaceUnigramCounts[token] + 1 
            if count > 0:
                score = score + math.log(count) 
            # need to consider additional add-one when calculate score
            score = score - math.log(self.total + self.additional) 
        return score