# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 18:16:38 2018

@author: yinjiang

Absolute Discounting Smoothing
Pabs(wi∣wi−1)=max(c(wi−1wi)−δ,0)/∑w′c(wi−1w′) + α*Pabs(wi)
The essence of Kneser-Ney is in the clever observation that we can take advantage 
of this interpolation as a sort of backoff model. When the first term (in this case,
the discounted relative bigram count) is near zero, the second term (the lower-order
model) carries more weight. Inversely, when the higher-order model matches strongly,
the second lower-order term has little weight.
Replace Pabs(wi) to Pcontinuation(wi)
Pcontinuation(wi)   = |{wi−1:c(wi−1,wi)>0}| / |{wj−1:c(wj−1,wj)>0}|
                    = # of bigrams which wi completes / # of total bigram types
                    
Example:
Pabs(Francisco) is high, it ansers how likely wi to appear
Pcon(Francisco) is low, it answers how likely wi to appear in an unfamiliar bigram context
Final Equation:
PKN(wi∣wi−1) = first item + lambda * second item 
where:
first item = max(c(wi−1wi)−δ,0) / ∑w′c(wi−1w′)
second item = Pcontinuation(wi) = |{wi−1:c(wi−1,wi)>0}| / |{wj−1:c(wj−1,wj)>0}|
lamda = λ(wi−1)=δ * |{w′:c(wi−1,w′)>0}| / c(wi-1)
"""

import math
from collections import defaultdict


class CustomLM(object):
    
    def __init__(self, corpus):
        
        """            
        Kenser Ney Smoothing Bigram language model, we replace the MLE unigram probability 
        with the ‘continuation probability’ that estimates how likely the unigram 
        is to continue a new context.
        If a word appears after a small number of contexts, then it should be 
        less likely to appear in a novel context
        """
        self.total = 0
        self.unigramCount = defaultdict(lambda:0)
        self.bigramCount = defaultdict(lambda: defaultdict(lambda: 0))
        self.reversebigramCount = defaultdict(lambda: defaultdict(lambda: 0))
        self.discounts = defaultdict(lambda: 0)
        self.lm = self.train(corpus)
        
    def train(self, corpus):
        
        """
        Takes a corpus and trains your language model.
        Counter(ngrams)： generate ngrams tokens and counts; dict{tuple:int}
        kgrams_counts: a list of dict {kgram tokens: counts}, k is from highest_order to 0
        probs: a list of kgrams dict {tokens:logprob}; ngram, (n-1) gram, ..., unigram 
        """
        # step 1: generate ngram model of dict {tokens:counts}
        lasttoken = '$'
        for sentence in corpus.corpus:
            for datum in sentence.data:
                token = datum.word
                self.unigramCount[token] = self.unigramCount[token]+1
                self.bigramCount[lasttoken][token] = self.bigramCount[lasttoken][token]+1
                self.reversebigramCount[token][lasttoken] = self.reversebigramCount[token][lasttoken]+1
                self.total += 1
                lasttoken = token
        # step 2: generate freq of freq table
        lasttoken = '$'
        for sentence in corpus.corpus:
            for datum in sentence.data:
                token = datum.word
                if self.bigramCount[lasttoken][token] <= 4:
                    value = self.bigramCount[lasttoken][token]
                    self.discounts[value] += 1
                lasttoken = token
                
    def score(self, sentence):
        """
        Takes a list of strings and returns the log-probability of the sentence
        using the language model.
        Absolute Discounting, but set different D depends on freq of freq
        """
        score = 0.0
        lasttoken = '$'
        discounts = self.calc_discounts(self.discounts)
        for token in sentence:
            biCount = self.bigramCount[lasttoken][token]
            if (biCount > 0):
                D = self.get_discount(discounts, biCount)
                biCount = biCount - D
            else:
                # avoid zero probability
                biCount = 0.0001
            lasttokenCount = self.unigramCount[lasttoken]
            # lasttokenCount == total frequency of bigram[lasttoken]; 
            # total frequency in bigram where w1=lasttoken
            # lasttokenCount = sum(self.bigramCount[lasttoken][*])
            if (lasttokenCount == 0):
                lasttokenCount=999999
            # this is continuation probability of token; 
            # self.total == len(unigramCount.items()); total tokens in the corpus
            p_wn = float(len(self.reversebigramCount[token].items()))/self.total
            r = D * len(self.bigramCount[lasttoken].items()) / lasttokenCount
            
            score = score + math.log(biCount/lasttokenCount + r * p_wn)
            lasttoken = token
            
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