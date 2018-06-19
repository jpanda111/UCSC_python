# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 17:54:18 2018
@author: yinjiang
"""

import math
from HolbrookCorpus import HolbrookCorpus
from EditModel import EditModel
from SpellResult import SpellResult
from UnigramLM import UnigramLM
from LaplaceUnigramLM import LaplaceUnigramLM
from LaplaceBigramLM import LaplaceBigramLM
from StupidBackoffLM import StupidBackoffLM
from StupidBackoffAddoneSmoothingLM import StupidBackoffSmoothLM
from KatzBackoffGoodTuringDiscount import KatzBackoffGTLM
from ModifiedKneserNeyLM import MKneserNeyLM

# Modified version of Peter Norvig's spelling corrector
# Here is the link:
# https://norvig.com/spell-correct.html

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
            if sentence.isEmpty():
                continue
            # get any possible spell error sentence
            errorSentence = sentence.getErrorSentence()
            # use specific language model to guess highest possible corrected sentence
            hypothesis = self.correctSentence(errorSentence)
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
                try:
                    editscore = math.log(editscore)
                except ValueError:
                    editscore = float('-inf')
                    print word
                    print " log-probabilities = 0, go check editModel output!"
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
    
def main():
      """
      Train all the implemented language models and test them on the test data.
      """
      # generate a corpus include a list of sentence where corrected word(misspelled word), including start/stop symbol
      # example: <s> lucky (luckily) enough it was mostly tinned (tin) food </s>
      
      # use try-except to see if file exist or path is right
      try: 
          f = open("./data/holbrook-tagged-train.dat","r")
          f.readlines()
          f.close()
      except IOError:
          print "Files not found. Check if in the right directory path!"
          
      trainPath = './data/holbrook-tagged-train.dat'
      trainCorpus = HolbrookCorpus(trainPath)
      testPath = './data/holbrook-tagged-dev.dat'
      testCorpus = HolbrookCorpus(testPath)
      
      with open('ComparisonLM.log','w') as f:
          
          f.write('Comparison of different language models: \n')
          f.write('\n')
          print ('Unigram Language Model Evaluation')
          f.write('Unigram Language Model: \n')
          unigramLM = UnigramLM(trainCorpus)
          unigramSpell = SpellCorrection(unigramLM, trainCorpus)
          unigramOutput,t = unigramSpell.evaluation(testCorpus)
          f.write(str(unigramOutput))
          f.write('\nTime to run (seconds): ')
          f.write(str(t)+'\n')
          f.write('\n')
          print ('Laplace Unigram Language Model Evaluation')
          f.write('Laplace Unigram Language Model: \n')
          LunigramLM = LaplaceUnigramLM(trainCorpus)
          LuniformSpell = SpellCorrection(LunigramLM, trainCorpus)
          LunigramOutput,t = LuniformSpell.evaluation(testCorpus)
          f.write(str(LunigramOutput))
          f.write('\nTime to run (seconds): ')
          f.write(str(t)+'\n')
          f.write('\n')
          print ('Laplace Bigram Language Model Evaluation')
          f.write('Laplace Bigram Language Model: \n')
          LbigramLM = LaplaceBigramLM(trainCorpus)
          LbigramSpell = SpellCorrection(LbigramLM, trainCorpus)
          LbigramOutput,t = LbigramSpell.evaluation(testCorpus)
          f.write(str(LbigramOutput))
          f.write('\nTime to run (seconds): ')
          f.write(str(t)+'\n')
          f.write('\n')
          print ('Stupid Backoff Language Model Evaluation')
          f.write('Stupid Backoff Language Model: \n')
          SBOLM = StupidBackoffLM(trainCorpus)
          SBOSpell = SpellCorrection(SBOLM, trainCorpus)
          SBOOutput,t = SBOSpell.evaluation(testCorpus)
          f.write(str(SBOOutput))
          f.write('\nTime to run (seconds): ')
          f.write(str(t)+'\n')
          f.write('\n')
          print ('Stupid Backoff with add-one smoothing Language Model Evaluation')
          f.write('Stupid Backoff with add-one smoothing Language Model: \n')
          SBOASLM = StupidBackoffSmoothLM(trainCorpus)
          SBOASSpell = SpellCorrection(SBOASLM, trainCorpus)
          SBOASOutput,t = SBOASSpell.evaluation(testCorpus)
          f.write(str(SBOASOutput))
          f.write('\nTime to run (seconds): ')
          f.write(str(t)+'\n')
          f.write('\n')
          print ('Modified Kneser Ney Smoothing Language Model Evaluation')
          f.write('Modified Kneser Ney Smoothing Language Model: \n')
          MKNLM = MKneserNeyLM(trainCorpus)
          MKNSpell = SpellCorrection(MKNLM, trainCorpus)
          MKNOutput,t = MKNSpell.evaluation(testCorpus)
          f.write(str(MKNOutput))
          f.write('\nTime to run (seconds): ')
          f.write(str(t)+'\n')
          f.write('\n')
          print ('Katz Backoff with Good-Turing smoothing Language Model Evaluation')
          f.write('Katz Backoff with Good-Turing smoothing Language Model: \n')
          KBOGTLM = KatzBackoffGTLM(trainCorpus)
          KBOGTSpell = SpellCorrection(KBOGTLM, trainCorpus)
          KBOGTOutput,t = KBOGTSpell.evaluation(testCorpus)
          f.write(str(KBOGTOutput))
          f.write('\nTime to run (seconds): ')
          f.write(str(t)+'\n')
          f.write('\n')
      
if __name__ == "__main__":
    main()
    
    
