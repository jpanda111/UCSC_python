'''
Create a base/parent class called 'InterestCalculator'. Create a child class 
called 'CICalculator'. CI stands for compound interest.  The 'CICalculator' 
class will have only one parent, the 'InterestCalculator'. Create a child 
class called 'SICalculator'. The 'SI' class will have only one parent, 
the 'InterestCalculator'. SI stands for simple interest. 
The parent class needs to have an __init__ method, 
that will initialize all the values needed for calculating and storing interest.

The child class 'CICalculator' and 'SICalculator' must implement 
'calcfinalval' method that will calculate the final value for each case.


Once all classes have been defined, the call to calculate and print 
the final value must follow the code below.

The arguments to the __init__ method are: number of years, interest rate 
and initial principal.

c = CICalculator(2,0.1,1000)
c.calcfinalval()
print c.finalval

s = SICalculator(2,0.1,1000)
s.calcfinalval()
print s.finalval
'''

class InterestCalculator:
    def __init__(self,years,rate,initialval):
        self.years = years
        self.rate = rate
        self.initialval = initialval
        self.finalval = 0 

# finalval = initialval(1 + rate*years)
class SICalculator(InterestCalculator):
    def calcfinalval(self):
        self.finalval = self.initialval *(1+self.rate*self.years)

class CICalculator(InterestCalculator):
    def calcfinalval(self):
        self.finalval = self.initialval *((1+self.rate)**self.years)

c = CICalculator(2,0.1,1000)
c.calcfinalval()
print c.finalval

s = SICalculator(2,0.1,1000)
s.calcfinalval()
print s.finalval

'''
A stack follows LIFO (last-in, first-out). LIFO is the case where the last  
element added is the first element that can be retrieved. 
Consider a list with values [4,6,9]. Create a class called Sclass with 
functions sadd and sretrieve to add and pop elements from the list 
in LIFO order respectively. After each function call, print the contents 
of the list. Add 12 to the queue and then follow the LIFO rules and 
pop elements until the list is empty. 
'''

class Sclass:    
    def __init__(self,a):
        self.a = a
        
    def sadd(self,b):
        self.a.extend([b])
        
    def sretrieve(self):
        while(len(self.a) > 0):
            print self.a.pop(-1)
            print self.a
                                     
a = [4,6,9]
c = Sclass(a)
c.sadd(12)
c.sretrieve()