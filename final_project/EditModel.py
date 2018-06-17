# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 19:14:22 2018

@author: yinjiang
"""

import collections

class EditModel(object):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    def __init__(self, edit_file="./data/count_1edit.txt", corpus=None):
        self.edit_file=edit_file
        self.edit_table=self.read_edit_table(self.edit_file)
        if corpus:
            self.initVocabulary(corpus)
        
    def initVocabulary(self, corpus):
        """
        Generate the initial set of word from the corpus
        """
        self.vocabulary = set()
        for sentence in corpus.corpus:
            for datum in sentence.data:
                self.vocabulary.add(datum.word)
 
    def read_edit_table(self, file_name):
        """
        Reads in the string edit counts file. 
        Returns a dictionary of 's1|s2' -> count.
        s1 is misspelled, s2 is correct
        """
        edit_table = collections.defaultdict(lambda:0)
        f = open(file_name, 'r')
        for line in f:
            contents = line.split("\t")
            # example: ul|u	83
            edit_table[contents[0]] = int(contents[1])
        return edit_table
    
    def edit_count(self, s1, s2):
        """
        Returns how many times substring s1 is edites as s2.
        """
        return self.edit_table[s1+"|"+s2]
    
    def getProbabilities(self, word):
        """
        Computes P(corrected-word|misspelled-word) edit model for a given word. 
        Returns a dictionary {corrected-word: P(corrected-word|misspelled-word)}
        Includes all the possible misspelled for this given word.
        """
        s=[(word[:i],word[i:]) for i in range(len(word)+1)]
        counts=collections.defaultdict(lambda:0)
        # deletions
        # example: hlello -> hello, l=b[0]
        for a,b in s:
            if b and a+b[1:] in self.vocabulary:
                tail = ''
                if len(a)>0:
                    tail=a[-1]
                original = tail + b[0] # hl
                replacement = tail # h
                count = self.edit_count(original, replacement)
                if count:
                    # a+b[1:] is correct spell, count is # of misspelled info from count_1edit.txt
                    counts[a+b[1:]] += count
        # transpositions
        # example: hlelo -> hello, l=b[0], e=b[1]
        for a,b in s:
            if len(b)>1 and a+b[1]+b[0]+b[2:] in self.vocabulary:
                # new word is a+b[1]+b[0]+b[2:]
                # edit is b[0]b[1] --> b[1]b[0]
                original = b[0] + b[1]
                replacement = b[1] + b[0]
                count = self.edit_count(original, replacement)
                if count:
                    counts[a+b[1]+b[0]+b[2:]] += count
        # substituitions
        # example: hillo -> hello, e=c, i=b[0]
        for a,b in s:
            if b:
                for c in self.alphabet:
                    if a+c+b[1:] in self.vocabulary:
                        # new word is a+c+b[1:]
                        original = b[0]
                        replacement = c
                        count = self.edit_count(original, replacement)
                        if count:
                            counts[a+c+b[1:]] += count
        # additions
        # example: hllo -> hello, e=c
        for a,b in s:
            for c in self.alphabet:
                if a+c+b in self.vocabulary:
                    # new word is a+c+b
                    tail= ''
                    if len(a)>0:
                        tail = a[-1]
                    original = tail
                    replacement = tail +c
                    count= self.edit_count(original, replacement)
                    if count:
                        counts[a+c+b] += count
        
        # normalize counts.
        # counts is dictionary {corrected spell: misspelled-counts}
        total = 0.0
        for a,b in counts.items():
            total += b
        selfCount = max(9*total, 1)
        counts[word] = selfCount
        total += selfCount
        probs = {}
        if (total != 0.0):
            for a,b in counts.items():
                probs[a] = float(b)/total
        return probs
    
    
        

    