# -*- coding: utf-8 -*-
"""
Created on Sat Jun 02 21:17:50 2018
@author: yinjiang
"""
# Question 1

class Quadratic(object):
    def __init__(self, a,b,c):
        self.a = a
        self.b = b
        self.c = c
    def __str__(self):
        """
        overwrite display method
        """
        if (self.a == 1):
            sa = "x^2"
        elif (self.a == -1):
            sa = "-x^2"
        else:
            sa = str(self.a)+"x^2"
        if (self.b == 1):
            sb = "+x"
        elif (self.b == -1):
            sb = "-x"
        elif (self.b == 0):
            sb = ""
        elif (self.b < 0 and self.b != -1):
            sb = str(self.b)+"x"
        else:
            sb = "+"+str(self.b)+"x"
        if (self.c > 0):
            sc = "+" + str(self.c)
        elif (self.c < 0):
            sc = str(self.c)
        else:
            sc = ""
        return sa+sb+sc
    def __add__(self,other):
        """
        operator overloading for addition operator
        """
        return "The Sum is %s" %Quadratic(self.a+other.a, self.b+other.b, self.c+other.c)
    def __sub__(self,other):
        """
        operator overloading for subtraction operator
        """
        return "The difference is %s" %Quadratic(self.a-other.a, self.b-other.b, self.c-other.c)
    def __eq__(self,other):
        """
        operator overloading for equal operator
        """
        return (self.a==other.a and self.b==other.b and self.c==other.c)

Q1 = Quadratic(3,8,-5)
Q2 = Quadratic(2,3,7)
quadsum = Q1 + Q2
quaddiff= Q1 - Q2
print(quadsum)
print(quaddiff)
Q1==Q1
Q1==Q2

# Question 2
     
class WordCounter(object):
    def __init__(self,filename):
        self.countdict = {}
        with open(filename, "r") as fo:
            a= [item.strip() for item in fo.readlines()]
        self.a = str(a)
        self.l = []
    def removepunctuation(self):
        """
        remove all the punctuations and leave only alphabets 
        and numbers in each word
        """
        import re
        punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' 
        regex = re.compile('[%s]' %re.escape(punctuation))
        self.l = regex.sub('', self.a)
    def findcount(self):
        """
        count the frequency of each word and store it in a 
        instance variable countdict
        """
        s = self.l.split(" ")
        for item in set(s):
            if item != "":
                self.countdict[item] = s.count(item)
    def writecountfile(self, csvfilename):
        """
        writes the content of countdict to a csv file with 
        two columns. The first one is the word and the second 
        is the count
        """
        with open(csvfilename,"wb") as csvfile:
            columnTitleRow="word, count\n"
            csvfile.write(columnTitleRow)
            for item in sorted(self.countdict, key = self.countdict.get, reverse=True):
                csvfile.write(item+ "," + str(self.countdict[item]) + "\n")

filename = "red-headed-league.txt"
w = WordCounter(filename)
w.removepunctuation()
w.findcount()
w.writecountfile("count-frequency-of-word.csv")
csv_file = "count-frequency-of-word.csv"
# two solutions to print out top 5 most popular words:
# solution 1 : using pandas module
import pandas as pd
data = pd.read_csv(csv_file, nrows=5)
print data
# solution 2: readlines one by one and stop after reading 6 lines
with open(csv_file, "rb") as csvfile:
    i=1
    for line in csvfile.readlines():
        if (i <= 6):
            array = line.split(",")
            word = array[0]
            print word
        else: break
        i+=1