'''
The standard form of a quadratic expression is ax^2 + bx + c where 
a, b and c are real numbers and a is not equal to zero. The degree of a 
quadratic expression is 2 and a, b and c are called the coefficients. 
For example, in the quadratic expression (3x^2 + 8x − 5), the 
coefficients are 3, 8 and -5 corresponding to the exponent 2, 1 an 0 
respectively. Define and use a Python class that can perform
operations on quadratic expressions such as addition and subtraction. Define 
a Python class called ‘Quadratic’. The Python object 
that will create this class will be as follows
Q1 = Quadratic(3,8,-5)
This corresponds to the expression above.
Define another Python object Q2 as follows
Q2 = Quadratic(2,3,7) which corresponds to the quadratic expression 
2x^2 + 3x + 7

Part I – Addition and subtraction of quadratic expressions
Perform the addition and subtraction operation by using 
operator overloading. Make the following Python calls:
quadsum = Q1+Q2
quaddiff = Q1-Q2
Print the values of quadsum and quaddiff. The output on your screen 
must be similar 
to the one below.
The sum is 5x^2+11x+2
The difference is x^2+5x-12

Part II – Equality operator for quadratic expressions
Two quadratic expressions are equal only if all the corresponding 
coefficients are equal. Define an equality operator that will return 
‘True’ if two quadratic expressions are equal and ‘False’ when they 
are not equal. For example, in this code for Q1 == Q1, the value must be ‘True’
and for Q1 == Q2, the value must be ‘False'.
'''

class Quadratic:
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return '%d x^2 + %d x + %d' %(self.a,self.b,self.c)

    def __add__(self,other):
        return Quadratic(self.a + other.a, self.b + other.b, self.c + other.c)

    def __sub__(self,other):
        return Quadratic(self.a - other.a, self.b - other.b, self.c - other.c)

    def __eq__(self,other):
        if(self.a == other.a and self.b == other.b and self.c == other.c):
            print "The two quadratics expression are equal"
            return True
        else:
            print "The two quadratics expression are not equal"
            return False

q1 = Quadratic(3, 8, -5)
q2 = Quadratic(2, 3, 7)

print "The sum of the given quadratic expressions is ", q1 + q2
print "The difference of the given quadratic expressions is ", q1 - q2
print q1 == q2

'''
Please ensure that you use space instead of tab for indentation. 
Then paste your code directly into the response box.

Write a program that will read the file, 
'red-headed-league.txt', count the frequency of the words and store 
it as a csv file.

Create a class called WordCounter with the following methods.

def __init__(self,filename) where filename is the name of the text file, 
'red-headed-league.txt'. This function should read the text file

def removepunctuation(self) must remove all the punctuations and leave 
only alphabets and numbers in each word

def findcount(self) must count the frequency of each word and store it 
in a instance variable called countdict

def writecountfile(self,csvfilename) writes the content of the countdict 
variable to a csv file with two columns. The first column is the word 
and second column is the count.

Create an instance of the class and call appropriate method
and store the result in a csv file. Printout the five most popular words. 
NOTE: DO NOT USE THE COUNTER DATA STRUCTURE IN COLLECTIONS MODULE.
'''

import string, csv

class WordCounter:
    def __init__(self,filename):
        self.filename = filename
        self.contentlist = []
        self.cleanlist = []
        self.countdict = {}
        fo = open(self.filename,'r')
        for lines in fo.readlines():
            lineitems = lines.strip().split()
            self.contentlist.extend(lineitems)

    def removepunctuation(self):
        for items in self.contentlist:
            cleanstring = items
            for c in string.punctuation:
                cleanstring = cleanstring.replace(c,"")
            if cleanstring != '':
                self.cleanlist.append(cleanstring)

    def findcount(self):
        uniqlist = list(set(self.cleanlist))
        print uniqlist
        for items in uniqlist:
            self.countdict[items] = self.cleanlist.count(items)

    def writecountfile(self,csvfilename):
        writer = csv.writer(open(csvfilename, 'wb'))
        for key, value in self.countdict.items():
            writer.writerow([key, value])

wc = WordCounter('red-headed-league.txt')
wc.removepunctuation()
wc.findcount()
print(wc.countdict)
wc.writecountfile('my4.csv')