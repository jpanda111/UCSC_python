# -*- coding: utf-8 -*-
"""
Created on Mon May 28 15:46:56 2018
@author: yinjiang

"""
# Question 1
class InterestCalculator(object):
    def __init__(self, years, rate, principal):
        self.years = years
        self.rate = rate
        self.principal = principal

class CICalculator(InterestCalculator):
    def calcfinalval(self):
        P = self.principal
        r = self.rate
        n = self.years
        self.finalval = P*(1+r)**n
        return self.finalval
    def __str__(self):
        return "The final value is %s" %self.finalval
class SICalculator(InterestCalculator):
    def calcfinalval(self):
        P = self.principal
        r = self.rate
        n = self.years
        self.finalval = P*(1+r*n)
        return self.finalval
    def __str__(self):
        return "The final value is %s" %self.finalval

c = CICalculator(2,0.1,1000)
c.calcfinalval()
print c.finalval

s = SICalculator(2,0.1,1000)
s.calcfinalval()
print s.finalval

# Question 2

class Sclass(object):
    def __init__(self, l):
        self.l = l
    def sadd(self, n):
        self.l.append(n)
        print self.l
    def sretrieve(self):
        self.l.pop()
        print self.l

l= [4,6,9]
s = Sclass(l)
s.sadd(12)
while len(s.l) > 0:
    s.sretrieve()

        