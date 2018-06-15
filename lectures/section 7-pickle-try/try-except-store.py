
# coding: utf-8

# In this notebook we will discuss 
# 
# 1. Error handling using try-except 
# 
# 2. Creating custom exceptions 
# 
# 3. Storing Python objects using 
# 
#     a. Pickle
#     
#     b. Shelve 

# What is an exception?
# 
# An exception is raised when a program has an error. Error handling is used to take care of 
# exceptions so that when there is no exception then the program runs smoothly and in case 
# of an error, the error handler can fix the problem or handle it so that the program can 
# be continued. 
# 
# try-except is a construct that handles exceptions.
# 
# Check this link 
# http://www.python-course.eu/exception_handling.php
# 
# List of Python builtin exceptions can be found at
# https://docs.python.org/2/library/exceptions.html

# In[ ]:

a = 10
b = 0
c = a/b

print c


# In[ ]:

'''
Instead of quitting after encountering the ZeroDivisionError, in this 
case we are assigning a new value to c so that the program can continue.
'''

try:
    c = a/b
except ZeroDivisionError:
    c = a

# Instead of quitting after encountering the ZeroDivisionError, in this 
# case we are assigning a new value to c so that the program can continue.

print c    


# In[ ]:

# Since the string can't be converted to an int, ValueError exception 
# will be raised
a = int('92384g')
print a, type(a)


# In[ ]:

try:
    a = int('92384g')
    b = 0
    c = a/b
except:
    print 'The error message is - Not a number.'
    print 'The error message is - Cannot divide by zero.'


# In[ ]:

try:
    a = int('92384g')
    b = 12
    c = 0
    d = b/c
except ValueError as v:
    print 'Not a number.  The error message is',v
except ZeroDivisionError as z:
    print 'Cannot divide by zero.  The error message is',z  


# In[ ]:

try:
    a = int('92384g')
except ValueError as v:
    print 'Not a number.  The error message is',v
    
b = 12
c = 0
try:   
    d = b/c
except ZeroDivisionError as z:
    print 'Cannot divide by zero.  The error message is',z


# try-except-else: the else clause has to placed after all the exceptions and 
# else clause will be executed when the try clause doesn't raise any exceptions
# 
# syntax
# ```
# try:
#     execute try statements
#     
# except exception1:
#     If there is exception1, then execute this block
# 
# except exception2:
#     If there is exception2, then execute this block
#     
# else:
#     If there is no exception, then execute this block
# ```

# In[ ]:

try:
    a = int('92')
except ValueError:
    a = 10
    print 'a is not a number. Gave a new value = ', a
else:
    print 'Is a number'
finally:
    print "I am all done"


# To enforce clean-up or termination clauses there is try-finally or 
# try-except-finally. Finally clause will be executed no matter whether an 
# exception occurs or not.
# 
# syntax
# ```
# try:
#     execute statements
#     
#     if an exception occurs, then this may be skipped
#     
# except e1:
#     statement to execute if there is an exception
# 
# else:
#     statements to execute if no exceptions are not raised
#     
# finally:
#         this will always be executed no matter whether an exception is 
#         raised or not
# ```

# In[ ]:

try:
    f = open("test1.txt","r")
    f.readlines()
    
except IOError:
    print "File not found."
    
finally:
    print "There is no file by this name."


# Note - the major difference between else clause and finally clause is that else clause will get executed only when no exceptions are raised. Whereas finally clause gets executed no matter whether an exception is raised or not. 

# In[ ]:

a = 10
b = 0
try:
    c = a/b
except ZeroDivisionError:
    c = a
finally:
    print c


# Custom Exceptions 
# 
# Custom exception has to be a class and it has to inherit from Python 
# Exception class.
# 
# Syntax for a simple custom exception without an error message
# 
# ```
# class exception_name(Exception):
#     pass
# ```
# 
# Syntax for a simple custom exception with an error message
# 
# ```
# class exception_name(Exception):
#     def __str__(self):
#         return "custom message"
# ```

# In[ ]:

class TooSmallError(Exception):
    pass

class TooLargeError(Exception):
    pass

def checkval(val,limit):
    if val < limit:
        raise TooSmallError
    else:
        raise TooLargeError
        

limit = 100
try:
    a = 50
    checkval(a,limit)
except TooSmallError:
    print "Too Small"
except TooLargeError:
    print "Too Large"    


# In[ ]:

'''
In-class activity for custom exception

You should ask user to input coefficients of a quadratic as a tuple. 
Then you check to see if the first coefficient is zero. If it is, 
then you should raise a custom exception. So you should write a 
custom exception class called CoeffZeroError. 
'''


# Pickle module
# 
# A pickle converts Python objects to bytes that can be stored or transmitted 
# (not secure). The CPickle module implemented using C is faster than pickle 
# that is implemented using Python. Pickle can handle unicode objects. 
# A "shelf" is a persistent, dictionary-like object. 
# 
# Check out the following links to learn more 
# https://freepythontips.wordpress.com/2013/08/02/what-is-pickle-in-python/
# 

# In[ ]:

try:
   import cPickle as pickle
except:
   import pickle


# In[ ]:

d1 = [ { 'a':'1', 'b':2, 'c':3 } ]
d2 = {'d':4,'e':5}

f = open('pickle.ck','wb')
pickle.dump(d1,f) # this command dumps d1 into the file pickle.ck
pickle.dump(d2,f) # this command dumps d2 into the file pickle.ck
f.close()

f = open('pickle.ck','rb')
nd1 = pickle.load(f)
nd2 = pickle.load(f)
f.close()

print 'Read values are:',
print nd1
print nd2


# In[ ]:

f = open('pickle.ck','rb')
n1 = pickle.load(f)
print n1
n2 = pickle.load(f)
print n2

'''
We have read all the information that needs to be read.  
The following will give an error.
'''

#nd3 = pickle.load(f) 
f.close()


# In[ ]:

tuple1 = (-2,4,10,)
f = open('pickle.ck','wb')
pickle.dump(tuple1,f)


# In[ ]:

f = open('pickle.ck','rb')
new1 = pickle.load(f)
print new1


# In[ ]:

'''
In-class activity on pickle - create a class called studentcourse. The class 
has to take the information: student name, year in college 
(freshman, sophomore, junior or senior) and two 
courses. Now store the information in a pickle file. The open the pickle 
file and print the contents. 
'''


# Shelve module can be used to store and retrieve Python objects easily.
# Shelve uses anydbm to store the data. Check out the following link 
# for more information.
# More reading material: 
# http://pymotw.com/2/shelve/

# In[ ]:

import shelve
d1 = { 'a':'1', 'b':2, 'c':3 }
list1 = ['apple', 'mango', 'pineapple']
s = shelve.open('fruit.sv') # opens the shelve
try:
    s['first'] = d1
    s['second'] = list1
finally:
    print s
    s.close()


# In[ ]:

import shelve
s = shelve.open('fruit.sv','r')
try:
    newd = s['first']
finally:
    s.close()
print newd


# In[ ]:

import shelve
d3 = [ { 'a':'1', 'b':2, 'c':3 } ]
# Write back uses in-memory cache. All items in cache are written to the shelve 
# when it is closed.
s = shelve.open('fruit.sv',writeback=True)
try:
    s['firstdict'] = d3
finally:
    s.close()


# In[ ]:

import shelve
s = shelve.open('fruit.sv')
if 'second' in s: # we are checking if the key second exists
    print s['second']


# In[ ]:

import shelve
s = shelve.open('fruit.sv')
if 'firstdict' in s: # we are checking if the key firstdict exists
    print s['firstdict']


# Note - the major difference between pickle and shelve is that pickle 
# stores the objects one at a time and objects can only be retrieved in 
# the order they were written. Whereas objects in shelve can be 
# accessed in any order. 

# In[ ]:

'''
In-class activity on shelve - create a class called studentcourse. The 
class has to take the information: student name, year in college 
(freshman, sophomore, junior or senior) and two courses. Now store the 
information in a shelve file. The open the shelve file and print the 
contents. Use the code from the in-class activity for pickle and 
modify it.
'''

