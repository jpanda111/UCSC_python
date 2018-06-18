# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 17:31:17 2018

@author: Dai
"""

import math, collections

class KatzBackoffLM(object):
    
    def __init__(self, corpus):
        
        """
        Katz Backoff Languange Model with Good-Turing smoothing is implemented.
        """
        
        self.UnigramCount = collections.defaultdict(lambda:0)
        self.BigramCount = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
        self.total = 0
        self.additional = 0
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
                self.UnigramCount[token] = self.UnigramCount[token] + 1
                self.BigramCount[lasttoken][token] = self.BigramCount[lasttoken][token] + 1
                self.total += 1
                lasttoken = token

    def score(self, sentence):
        """
        Takes a list of strings and returns the log-probability of the sentence
        using the language model.
        In Katz Backoff language model, Good-Turing smoothing technique applied to unseen words.
        """
        # total tokens inside language model, additional counts added when using add-one smoothing
        self.additional = len(list(self.LaplaceUnigramCount.items()))
        # total counts inside unigram model
        self.total = sum(v for v in self.LaplaceUnigramCount.values())
        score = 0.0
        for token in sentence:
            count = self.LaplaceUnigramCount[token] + 1 # Add-one smoothing for unseen words
            score = score + math.log(count) - math.log(self.total + self.additional) # need to consider additional add-one when calculate score
        return score
        
    def calc_discounts(self, num_with_count):
        
        """
        Calculates the optimal discount values for kgrams with counts 1, 2, & 3+
        num_with_count: freq of freq of words with freq <= 4
        Returns discounts depends on freq which is the 'modified' kneser-Ney smoothing
        """
        Y = num_with_count[1]/float(num_with_count[1] + 2 * num_with_count[2])
        # set freq of freq 0 = 0
        discounts= [0]
        # calculates discounts based on freq of freq: =1, =2, >=3;
        for i in range(1,4):
            if num_with_count[i] == 0:
                discount = 0
            else:
                discount = i-(i+1)*Y*num_with_count[i+1]/num_with_count[i]
            discounts.append(discount)
        if any(d for d in discounts[1:] if d <= 0):
        # try all(d for d in discounts[1:] if d > 0)
            raise Exception(
                    '***Warning Messsage*** Negative Discount observed. '
                    'Need to check data set and find out rootcause!')
        return discounts 
        
    def get_discount(self, discounts, count):
        
        if count > 3:
            return discounts[3]
        return discounts[count]