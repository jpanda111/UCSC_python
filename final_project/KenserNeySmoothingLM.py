# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 11:00:45 2018

@author: yinjiang

Material to read:
http://smithamilli.com/blog/kneser-ney/

"""

import math, collections

class KenserNeySmoothingLM(object):
    
    def __init__(self, corpus):
        
        """
        KenserNey Smoothing Bigram Languange Model 
        with absolute discounting is implemented.
        """
        
        self.total = 0
        self.unigramCount = collections.defaultdict(lambda: 0)
        self.bigramCount = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
        self.reversebigramCount = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
        self.train(corpus)
        
    def train(self, corpus):
        """
        Takes a corpus and trains your language model
        Compute any counts or other corpus statistics in this function
        """
        lasttoken = '$'
        for sentence in corpus.corpus:
            for datum in sentence.data:
                token = datum.word
                self.unigramCount[token] = self.unigramCount[token] + 1
                self.bigramCount[lasttoken][token] = self.bigramCount[lasttoken][token] + 1
                self.reversebigramCount[token][lasttoken] = self.reversebigramCount[token][lasttoken] + 1
                self.total += 1
                lasttoken = token
        
    def score(self, sentence):
        """
        Takes a list of strings and returns the log-probability of the sentence
        using the language model.
        Absolute Discounting, set D=0.75, do not differeniate D depends on freq of freq
        """
        score = 0.0
        lasttoken = '$'
        D = 0.75
        for token in sentence:
            biCount = self.bigramCount[lasttoken][token]
            if (biCount > 0):
                biCount = biCount - D
            else:
                biCount = 0.0001
            lasttokenCount = self.unigramCount[lasttoken]
            # lasttokenCount == total frequency of bigram[lasttoken]; total frequency in bigram where w1=lasttoken
            # lasttokenCount = sum(self.bigramCount[lasttoken][*])
            if (lasttokenCount == 0):
                lasttokenCount=999999
            p_wn = float(len(self.reversebigramCount[token].items()))/self.total
            # self.total == len(unigramCount.items()); total tokens in the corpus
            r = D * len(self.bigramCount[lasttoken].items()) / lasttokenCount
            
            score = score + math.log(biCount/lasttokenCount + r * p_wn)
            lasttoken = token
            
        return score
            
            