# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 17:54:18 2018

@author: yinjiang
"""

import math
from Datum import Datum 
from Sentence import Sentence
from HolbrookCorpus import HolbrookCorpus
from EditModel import EditModel
from SpellResult import SpellResult
import types
from UniformLM import UniformLM
from UnigramLM import UnigramLM
from LaplaceBigramLM import LaplaceBigramLM
from LaplaceTrigramLM import LaplaceTrigramLM
from LaplaceUnigramLM import LaplaceUnigramLM
from StupidBackoffLM import StupidBackoffLM
from KenserNeySmoothingLM import KenserNeySmoothingLM
from CustomLM import CustomLM


# Modified version of Peter Norvig's spelling corrector
"""Spelling Corrector.
Copyright 2007 Peter Norvig. 
Open source code under MIT license: http://www.opensource.org/licenses/mit-license.php
"""

import re, collections

class SpellCorrection:
    """
    Holds edit model, language model, corpus, trains
    """
    
    def __init__(self, lm, corpus):
        self.lm = lm
        self.editModel = EditModel("./data/count_1edit.txt", corpus)
        
    def evaluation(self, corpus):
        
        """
        Tests this speller on a corpus
        Returns a spelling result
        """
        
        numCorrect = 0
        numTotal = 0
        testData = corpus.generateTestCases()
        for sentence in testData:
            #print sentence
            if sentence.isEmpty():
                continue
            # get any possible spell error sentence
            errorSentence = sentence.getErrorSentence()
            #print errorSentence
            # use specific language model to guess highest possible corrected sentence
            hypothesis = self.correctSentence(errorSentence)
            #print hypothesis
            # use test data to check correctness
            if sentence.isCorrection(hypothesis):
                numCorrect += 1
            numTotal += 1
        return SpellResult(numCorrect, numTotal)
        
    def correctSentence(self, sentence):
        
        """
        Takes a list of words, including words or error
        Returns a corrected list of words.
        """
        
        if len(sentence) == 0:
            return []
        argmax_index = 0
        argmax_word = sentence[0]
        maxscore = float('-inf')
        maxlm = float('-inf')
        maxedit = float('-inf')
        
        # skip start and end tokens
        for i in range(1, len(sentence)-1):
            word = sentence[i]
            # return a dictionary {corrected-word: P(corrected-word|misspelled-word)} given a might-mis-spelled word
            editProbs = self.editModel.getProbabilities(word) 
            for alternative, editscore in editProbs.items():
                # no mis-spell happened, pass
                if alternative == word:
                    continue
                sentence[i] = alternative
                # get score of the corrected-sentence from language model
                lmscore = self.lm.score(sentence)
                if editscore != 0:
                    editscore = math.log(editscore)
                else:
                    editscore = float('-inf')
                # P_final=P(corrected_sentence)*P(corrected-word|misspelled-word);
                score = lmscore + editscore
                # find the highest one and store it
                if score >= maxscore:
                    maxscore = score
                    maxlm = lmscore
                    maxedit = editscore
                    argmax_index = i
                    argmax_word = alternative
            sentence[i] = word 
            argmax = list(sentence)
            # correct the spell error given might-mis-spelled word
            argmax[argmax_index] = argmax_word
        return argmax
    
    def correctCorpus(self, corpus):

        """
        Corrects the whole corpus, return a JSON representation of the output
        """   
        
        string_list=[]
        sentences = corpus.corpus
        for sentence in sentences:
            uncorrected = sentence.getErrorSentence()
            corrected = self.correctSentence(uncorrected)
            # join with , bookended with []
            word_list = '["%s"]' %'","'.join(corrected)
            string_list.append(word_list)
        output = '[%s]' % ','.join(string_list)
        return output
    
def main():
      """
      Train all the implemented language models and test them on the test data.
      """
      # generate a corpus include a list of sentence where corrected word(misspelled word), including start/stop symbol
      # example: <s> lucky (luckily) enough it was mostly tinned (tin) food </s>
      trainPath = './data/holbrook-tagged-train.dat'
      trainCorpus = HolbrookCorpus(trainPath)
      testPath = './data/holbrook-tagged-dev.dat'
      testCorpus = HolbrookCorpus(testPath)
      
      print('Custome Language Model: ')
      CLM = CustomLM(trainCorpus)
      CustomSpell = SpellCorrection(CLM, trainCorpus)
      CustomOutput = CustomSpell.evaluation(testCorpus)
      print(str(CustomOutput))
      
      print('Laplace Bigram Language Model: ')
      LbigramLM = LaplaceBigramLM(trainCorpus)
      LbigramSpell = SpellCorrection(LbigramLM, trainCorpus)
      LbigramOutput = LbigramSpell.evaluation(testCorpus)
      print(str(LbigramOutput))
      
      print('Laplace Trigram Language Model: ')
      LtrigramLM = LaplaceTrigramLM(trainCorpus)
      LtrigramSpell = SpellCorrection(LtrigramLM, trainCorpus)
      LtrigramOutput = LtrigramSpell.evaluation(testCorpus)
      print(str(LtrigramOutput))
      
      print('Uniform Language Model: ')
      # train the language model
      uniformLM = UniformLM(trainCorpus)
      # use the language model, guess highest prob of corrected-sentence based on language models and train data
      uniformSpell = SpellCorrection(uniformLM, trainCorpus)
      # use test data to get accuracy
      uniformOutput = uniformSpell.evaluation(testCorpus)
      print(str(uniformOutput))
      
      print('Unigram Language Model: ')
      unigramLM = UnigramLM(trainCorpus)
      unigramSpell = SpellCorrection(unigramLM, trainCorpus)
      unigramOutput = unigramSpell.evaluation(testCorpus)
      print(str(unigramOutput))
      
      print('Laplace Unigram Language Model: ')
      LunigramLM = LaplaceUnigramLM(trainCorpus)
      LuniformSpell = SpellCorrection(LunigramLM, trainCorpus)
      LunigramOutput = LuniformSpell.evaluation(testCorpus)
      print(str(LunigramOutput))
      
      print('Stupid Backoff Language Model: ')
      SBOLM = StupidBackoffLM(trainCorpus)
      SBOSpell = SpellCorrection(SBOLM, trainCorpus)
      SBOOutput = SBOSpell.evaluation(testCorpus)
      print(str(SBOOutput))
            
      print('Kenser Ney Smoothing Language Model: ')
      KNSLM = KenserNeySmoothingLM(trainCorpus)
      KNSSpell = SpellCorrection(KNSLM, trainCorpus)
      KNSOutput = KNSSpell.evaluation(testCorpus)
      print(str(KNSOutput))
      
if __name__ == "__main__":
    main()
    
    
