# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 13:01:57 2018

@author: yinjiang
"""

import math, random
from collections import Counter, defaultdict
import itertools

class ModifiedKneserNeyLM(object):
    
    def __init__(self, highest_order, ngrams, start_pad_symbol = '<s>', end_pad_symbol = '</s>'):
        
        """
        Constructor of KneserNeyLM
            highest_order: int, the order of the language model.
            ngrams: list -> tuple -> string, Ngrams of highest_order.
            start_pad_symbol: string, the symbol used to pad the beginning of the sentence.
            end_pad_symbol: string, the symbol used to pad the end of the sentence.
            
        In kenser Ney Smoothing language model,  we replace the MLE unigram probability 
        with the ‘continuation probability’ that estimates how likely the unigram 
        is to continue a new context.
        If a word appears after a small number of contexts, then it should be 
        less likely to appear in a novel context
        """
        self.highest_order = highest_order
        self.start_pad_symbol = start_pad_symbol
        self.end_pad_symbol = end_pad_symbol
        self.lm = self.train(ngrams)
        
    def train(self, ngrams):
        
        """
        Train the language model on the given ngrams.
        """
        kgram_counts = self.calc_adj_counts(Counter(ngrams))
        probs = self.calc_prob(kgram_counts)
        return probs
    
    def calc_adj_counts(self, highest_order_counts):
        
        """
        Calculates the adjusted counts for all ngrams up to the highest order.
            highest_order_counts: dict{tuple -> string : int}
            kgrams_counts: [list-> dict] list of dict from kgram to counts, k is from highest_order to 0
        """
        kgrams_counts = [highest_order_counts]
        for i in range(1, self.highest_order):
            last_order = kgrams_counts[-1]
            new_order = defaultdict(int)
            for ngram in last_order.keys():
                suffix = ngram[1:]
                new_order[suffix] += 1
            kgrams_counts.append(new_order)
        return kgrams_counts
        
    def calc_unigram_probs(self, unigrams):
        
        """
        Calculates unigram probability (normal MLE prob)
        Returns dict {token: prob}
        """
        total = sum(v for v in unigrams.values())
        unigrams = dict((k, math.log(v/total)) for k,v in unigrams.items())
        
        return unigrams
    
    def get_discount(self, discounts, count):
        
        if count > 3:
            return discounts[3]
        return discounts[count]
    
    def calc_discounts(self, num_with_count):
        
        """
        Calculates the optimal discount values for kgrams with counts 1, 2, & 3+
        """
        
        Y = num_with_count[1]/(num_with_count[1] + 2 * num_with_count[2])
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
            raise Exception(
                    '***Warning*** Non-positive D observed. '
                    'Dataset probably too small.')
        return discounts
    
    def calc_order_backoff_probs(self, order):
        
        """
        Calculate backoff model prefix probability.
        Return dict {prefix:prob}
        """
        # generate freq of freq of words which freq <= 4
        num_kgrams_with_count = Counter(value for value in order.values() if value <= 4)
        # generate discounts list
        discounts = self.calc_discounts(num_kgrams_with_count)
        prefix_sums = defaultdict(int)
        backoffs = defaultdict(int)
        for key in order.keys():
            prefix = key[:-1]
            count = order[key]
            prefix_sums[prefix] = prefix_sums[prefix] + count
            discount = self.get_discount(discounts, count)
            order[key] = order[key] - discount
            backoffs[prefix] = backoffs[prefix] + discount
            
        for key in order.keys():
            prefix = key[:-1]
            order[key] = math.log(order[key]/prefix_sums[prefix])
        for prefix in backoffs.key():
            # calculate lambda, aka left-over prob to (k-1) gram model
            backoffs[prefix] = math.log(backoffs[prefix]/prefix_sums[prefix])
        return backoffs
            
    def interpolate(self, orders, backoffs):
        
        for last_order, order, backoff in itertools.izip(
                reversed(orders), reversed(orders[:-1]), reversed(backoffs[:-1])):
            for key in order.keys():
                prefix, suffix = key[:-1], key[1:]
                order[key] = order[key] + last_order[suffix] + backoff[prefix]
        
    def calc_probs(self, orders):
        
        """
        Calculates interpolated probabilities of kgrams for all orders.
        """   
        backoffs = []
        # get all ngram prob except unigram
        for order in orders[:-1]:
            backoff = self.calc_order_backoff_probs(order)
            backoffs.append(backoff)
        # get unigram prob
        orders[-1] = self.calc_unigram_probs(orders[-1])
        backoffs.append(defaultdict(int))
        # get interpolated prob
        self.interpolate(orders, backoffs)
        return orders
    
    def logprob(self, ngram):
        for i, order in enumerate(self.lm):
            if ngram[i:] in order:
                return order[ngram[i:]]
        return None
    
    def score_sent(self, sent):
        
        """
        Return log prob of the sentence
        sent: tuple -> string, the words in the unpadded sentence.
        """
        #padded = ((self.start_pad_symbol,)*(self.highest_order-1)+sent+(self.end_pad_symbol,))
        sent_logprob = 0
        for i in range(len(sent) - self.highest_order + 1):
            ngram = sent[i:i+self.highest_order]
            sent_logprob = sent_logprob + self.logprob(ngram)
        return sent_logprob
    
    def get_context(self, sentence):
        
        """
        Extract context to predict next word from sentence.
        sentence: tuple -> string, words currently in sentence.
        Return the last words needed for LM (prefix for highest order LM)
        """
        return sentence[(len(sentence)-self.highest_order+1):]
        
    def generate_next_word(self, sent, probs):
        context = tuple(self.get_context(sent))
        # find all the prefix==context word and probs
        pos_ngrams = list((ngram, logprob) for ngram, logprob in probs.items() if ngram[:-1]==context)

        # Subtract max logprob from all logprobs to avoid underflow
        _, max_logprob = max(pos_ngrams, key=lambda x: x[1])
        pos_ngrams = list((ngram, math.exp(prob-max_logprob)) for ngram, prob in pos_ngrams)
        # Normalize to get conditional probability.
        total_prob = sum(prob for ngram, prob in pos_ngrams)
        pos_ngrams = list((ngram, prob/total_prob) for ngram, prob in pos_ngrams)
        rand = random.random()
        for ngram, prob in pos_ngrams:
            rand = rand-prob
            if rand < 0:
                return ngram[-1]
        return ngram[-1]
        
    def highest_order_probs(self):
        return self.lm[0]
    
    def generate_sentence(self, min_length=4):
        """
        Generate a sentence using the probabilities in the language model
        min_length: int, the minimum number of words in the sentence.
        """
        sent = []
        probs = self.highest_order_probs()
        while len(sent) < min_length + self.highest_order:
            sent = [self.start_pad_symbol]*(self.highest_order-1)
            sent.append(self.generate_next_word(sent,probs))
            while sent[-1] != self.end_pad_symbol:
                sent.append(self.generate_next_word(sent,probs))
        sent = " ".join(sent[(self.highest_order-1):-1])
        return sent
            
        
    
    
## how to test it
from nltk.corpus import gutenberg
from nltk.util import ngrams
from ModifiedKneserNeyLM import ModifiedKneserNeyLM

gut_ngrams = (ngram for sent in gutenberg.sents() for ngram in ngrams(sent, 3, pad_left=True, pad_right=True, pad_symbol='<s>'))
lm = ModifiedKneserNeyLM(3, gut_ngrams, end_pad_symbol='<s>')
print(lm.score_sent(('This','is','a','sample','sentence','.')))
      
            
                
        
        
        
        
