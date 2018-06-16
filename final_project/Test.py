# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 18:38:05 2018
@author: yinjiang

UCSC Pyton Programming Final Project

Requirement (at least 6 python elements from the following)
1.  // Use any data structure like list, dictionary, set or tuple
2.  // List comprehension 
3.  Dictionary comprehension
4.  // Functions
5.  // Classes
6.  User created iterators
7.  // Importing external modules
8.  // Error checks using try-except
9.  // File input and output
10. // Regular expression
11. // Itertools 
12. // Decorators

Overview
Train different type of lanuage models and as part of noisy-channel model for 
spelling correction. 
Evaluate those language models by given a sentence with exactly one typing error, 
and calculate the accuracy.
Accuracy = the number of valid corrections / the number of test sentences.

Data
Utilize the writings of secondary-school children, collected by David Holbrook.
- holbrook-tagged-train.dat: the corpus to train the language models
- holbrook-tagged-dev.dat: a corpus of spelling errors for development
- count_1edit.txt: a table listing counts of edits x|w, taken from Wikepedia.
Note the data files do not contain <s> and </s> markers, but the code which
reads in the data adds them.

Code
- SpellCorrect.py:
    Computes the most likely correction given a lanuage model and
edit model. The main() function will load all of your language model and print performance.
- EditModel.py: 
    Reads the count_1edit.txt file and computes the probability of corrections.
The candidate corrections are all strings within Damerau-Levenshtein edit distance. The 
probability of no correction is set at .9.
- HolbrookCorpus.py: 
    Reads in the corpus and generates test cases from misspellings.
- Sentence.py: 
    Holds the data for a given sentence, which is a list of Datums. Contains
helper functions for generating the correct sentence and the sentence with the spelling error.
- Datum.py: 
    Contains two strings, word and error. The word is the corrected word, and error contains
the spelling error. For tokens which are spelled correctly in the corpus, error=''.
- SpellResult.py:
    Calculate specific language model's accuracy.
    
Language Models built
- Laplace Unigram Language Model:
    A unigram model with add-one smoothing. Treat out-of-vocabulary items as a word which was
seen zero times in training.
- Laplace Bigram Language Model:
    A bigram model with add-one smoothing.
- Stupid Backoff Language Model:
    Use an unsmoothed bigram model combined with backoff to an add-one smoothed unigram model
- Custom Language Model:
    interpolated Knerser-Ney, Good-Turing, Linear Interpolated, trigram

"""


