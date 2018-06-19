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

class KatzBackoffGTLM(object):
    
    def __init__(self, corpus):
        
        """            
        Katz Backoff Bigram language model with Good-Turing Discounts techniques.
        The discounts only applied for freq <=5, others still use Pmle probabilities.
        """
        self.total = 0
        self.discounts1 = []
        self.discounts2 = []
        self.unigramCount = defaultdict(lambda:0)
        self.bigramCount = defaultdict(lambda: defaultdict(lambda: 0))
        self.lm = self.train(corpus)
        
    def train(self, corpus):
        
        """
        Takes a corpus and trains your language model.
        Counter(ngrams)： generate ngrams tokens and counts; dict{tuple:int}
        kgrams_counts: a list of dict {kgram tokens: counts}, k is from highest_order to 0
        probs: a list of kgrams dict {tokens:logprob}; ngram, (n-1) gram, ..., unigram 
        """
        # step 1: generate ngram model of dict {tokens:counts}
        lasttoken = '<s>'
        for sentence in corpus.corpus:
            for datum in sentence.data:
                token = datum.word
                self.unigramCount[token] = self.unigramCount[token]+1
                self.bigramCount[lasttoken][token] = self.bigramCount[lasttoken][token]+1
                self.total += 1
                lasttoken = token
        # step 2: generate freq of freq table on unigram and bigram
        lasttoken = '<s>'
        Discounts1 = defaultdict(lambda: 0)
        Discounts2 = defaultdict(lambda: 0)
        for sentence in corpus.corpus:
            for datum in sentence.data:
                token = datum.word
                if self.bigramCount[lasttoken][token] <= 6:
                    value = self.bigramCount[lasttoken][token]
                    Discounts2[value] += 1
                if self.unigramCount[token] <= 6:
                    value = self.unigramCount[token]
                    Discounts1[value] += 1
                lasttoken = token
        # get a list of freq of freq table
        self.discounts2 = self.calc_discounts(Discounts2)
        self.discounts1 = self.calc_discounts(Discounts1)  
        
    def score(self, sentence):
        """
        Takes a list of strings and returns the log-probability of the sentence
        using the language model.
        Absolute Discounting, but set different D depends on freq of freq
        """
        score = 0.0
        lasttoken = '<s>'
        for token in sentence:
            biCount = self.bigramCount[lasttoken][token]
            uniCount = self.unigramCount[token]
            if (biCount > 0):
                biCount = self.get_adjcount(self.discounts2, biCount)
                score = score + math.log(biCount) - math.log(self.unigramCount[lasttoken])
            elif (uniCount>0):
                # calculate adjcount of unigram
                uniCount = self.get_adjcount(self.discounts1, uniCount)
                # calculate bigram left-over prob first
                GroupinBi = self.bigramCount[lasttoken]
                orgtotal = sum(v for v in GroupinBi.values())
                if orgtotal > 0:
                    adjtotal = sum(self.get_adjcount(self.discounts2, v) for v in GroupinBi.values())
                    leftover = 1- adjtotal/orgtotal
                    # remove duplicated token in bigram to avoid double calculation
                    adjprob = sum(self.get_adjcount(self.discounts1, j)/float(self.total) for i,j in self.unigramCount.items() if i not in GroupinBi)
                else:
                    leftover = 1
                    adjprob = sum(self.get_adjcount(self.discounts1, v)/float(self.total) for v in self.unigramCount.values())
                alpha = leftover /adjprob
                score = score + math.log(alpha * uniCount)- math.log(self.total)
            lasttoken = token
            
        return score
        
    def calc_discounts(self, num_with_count):
        
        """
        Calculates the Good-Turing discount ratios for kgrams with counts 1, 2, 3, 4, 5;
        Larger than 5: reliable enough to use Pmle, no adjustment.
        num_with_count: freq of freq of words with freq <= 6
        Returns discounts ratio depends on freq which is the Good-Turing smoothing
        d = r*/r = (r+1)*(n_r+1)/r*(n_r)
        """
        # set freq of freq 0 = 0
        discounts= [0]
        # calculates discounts based on freq of freq: =1, =2, =3, =4, =5;
        for i in range(1,6):
            if num_with_count[i] == 0:
                discount = 0
            else:
                # 0 < discount < 1
                discount = (i+1) * num_with_count[i+1]/float(i*num_with_count[i]) 
            discounts.append(discount)
        if any(d for d in discounts[1:] if d <= 0):
            raise Exception(
                    '***Warning*** Non-positive D observed. '
                    'Dataset probably too small.')
        return discounts 
        
    def get_adjcount(self, discounts, count):
        
        if count > 5:
            return count
        return discounts[count]*count
      
            
                
        
        
        
        
