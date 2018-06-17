# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 21:04:48 2018

@author: yinjiang
"""

import math

class UniformLM(object):
    
    def __init__(self, corpus):
        
        """
        Template for general language model
        """
        
        self.words = set([])
        self.train(corpus)
        
    def train(self, corpus):
        """
        Takes a corpus and trains your language model
        Compute any counts or other corpus statistics in this function
        """
        # self.words=[d.word for d in s.data for s in corpus.corpus]
        for sentence in corpus.corpus:
            for datum in sentence.data:
                word = datum.word
                self.words.add(word)
    
    def score(self, sentence):
        """
        Takes one sentence and returns the log-probability of the sentence
        using the language model.
        """
        score = 0.0
        probability = math.log(1.0/len(self.words))
        for word in sentence:
            score += probability
        return score