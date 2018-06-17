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

def timeit(func):
    import time
    def wrapper(*args):
        t = time.clock()
        res = func(*args)
        #print "The time to run the function: '%s' is %s seconds" %(func.func_name, time.clock()-t)
        t1 = time.clock()-t
        return res, t1
    return wrapper

class SpellCorrection:
    """
    Holds edit model, language model, corpus, trains
    """
    
    def __init__(self, lm, corpus):
        self.lm = lm
        self.editModel = EditModel("./data/count_1edit.txt", corpus)
    
    @timeit    
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
      
      with open('ComparisonLM.log','w') as f:
          f.write('Comparison of different language models: \n')
          
          f.write('Laplace Bigram Language Model: \n')
          LbigramLM = LaplaceBigramLM(trainCorpus)
          LbigramSpell = SpellCorrection(LbigramLM, trainCorpus)
          LbigramOutput,t = LbigramSpell.evaluation(testCorpus)
          f.write(str(LbigramOutput))
          f.write('\nTime to run (seconds): ')
          f.write(str(t)+'\n')
          
          f.write('Modified Kneser Ney Smoothing Language Model: \n')
          CLM = CustomLM(trainCorpus)
          CustomSpell = SpellCorrection(CLM, trainCorpus)
          CustomOutput,t = CustomSpell.evaluation(testCorpus)
          f.write(str(CustomOutput))
          f.write(str(t)+'\n')
          
          f.write('Laplace Trigram Language Model: \n')
          LtrigramLM = LaplaceTrigramLM(trainCorpus)
          LtrigramSpell = SpellCorrection(LtrigramLM, trainCorpus)
          LtrigramOutput,t = LtrigramSpell.evaluation(testCorpus)
          f.write(str(LtrigramOutput))
          f.write('\nTime to run (seconds): \n')
          f.write(str(t)+'\n')
          
          f.write('Uniform Language Model: \n')
          # train the language model
          uniformLM = UniformLM(trainCorpus)
          # use the language model, guess highest prob of corrected-sentence based on language models and train data
          uniformSpell = SpellCorrection(uniformLM, trainCorpus)
          # use test data to get accuracy
          uniformOutput,t = uniformSpell.evaluation(testCorpus)
          f.write(str(uniformOutput))
          f.write('\nTime to run (seconds): \n')
          f.write(str(t)+'\n')
          
          f.write('Unigram Language Model: \n')
          unigramLM = UnigramLM(trainCorpus)
          unigramSpell = SpellCorrection(unigramLM, trainCorpus)
          unigramOutput,t = unigramSpell.evaluation(testCorpus)
          f.write(str(unigramOutput))
          f.write('\nTime to run (seconds): \n')
          f.write(str(t)+'\n')
          
          f.write('Laplace Unigram Language Model: \n')
          LunigramLM = LaplaceUnigramLM(trainCorpus)
          LuniformSpell = SpellCorrection(LunigramLM, trainCorpus)
          LunigramOutput,t = LuniformSpell.evaluation(testCorpus)
          f.write(str(LunigramOutput))
          f.write('\nTime to run (seconds): \n')
          f.write(str(t)+'\n')
          
          f.write('Stupid Backoff Language Model: \n')
          SBOLM = StupidBackoffLM(trainCorpus)
          SBOSpell = SpellCorrection(SBOLM, trainCorpus)
          SBOOutput,t = SBOSpell.evaluation(testCorpus)
          f.write(str(SBOOutput))
          f.write('\nTime to run (seconds): \n')
          f.write(str(t)+'\n')
                
          f.write('Kenser Ney Smoothing Language Model: \n')
          KNSLM = KenserNeySmoothingLM(trainCorpus)
          KNSSpell = SpellCorrection(KNSLM, trainCorpus)
          KNSOutput,t = KNSSpell.evaluation(testCorpus)
          f.write(str(KNSOutput))
          f.write('\nTime to run (seconds): \n')
          f.write(str(t)+'\n')
      
if __name__ == "__main__":
    main()
    
    
