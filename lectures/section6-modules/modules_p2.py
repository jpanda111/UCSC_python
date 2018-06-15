
# coding: utf-8

# In this notebook we will discuss following modules:
# 
# 1) random
# 
# 2) time
# 
# 3) datetime
# 
# 4) urllib2
# 
# 5) uuid
# 
# 6) matplotlib
# 
# 7) lxml
# 
# Interesting links for random module
# 
# http://pymotw.com/2/random/
# http://www.pythonforbeginners.com/random/how-to-use-the-random-module-in-python
# 

# In[ ]:

import random
# Generate a random floating point value
print random.random()


# random.seed will ensure that the random number generation process is the 
# same at every run. This is done to make sure that the number generated is 
# independent of the machine on which the code is run.

# In[ ]:

random.seed(1)
print random.random()


# random.randint(low, high = None, size = None)
# both low value and high value are inclusive generates a random integer value.

# In[ ]:

print random.randint(1,10)


# Just like range, for randrange you can give one value which would be considered as a stop value or you could give two values, the first value will be the start value and the second value will be the stop value
# 
# ```random.randrange ([start,] stop [,step])```
# 
# start value is inclusive, stop value is exclusive and step size is optional.

# In[ ]:

print random.randrange(10)
print random.randrange(0, 10)


# In[ ]:

# Generate a random integer value between 0 and 10 in steps of 2.
random.randrange(0, 10, 2)


# In[ ]:

a = [1,2,30,5]
# Pick a random value from the list
print random.choice(a)


# In[ ]:

'''
In-class activity: Take five numbers from the user and make it into a
list. Randomly select a number from the list. Write a function to compute
2 power that number. And show the result to the user. 
'''


# Time Module - provides various time-related functions.
# 
# time.time returns the time in seconds since the epoch, i.e., the point where the time starts which is 1 January 1970 for all the operating systems.

# In[ ]:

import time
print time.time()


# time.clock() returns the wall-clock time expressed in seconds elapsed since 
# the first call to this function. It is useful for timing operations.

# In[ ]:

print time.clock()


# If you want to find out how much time a process takes then you can note 
# the clock time at the start of the process and then note the clock time 
# after the process and take the difference of clock time. 

# In[ ]:

# Note down starting time
t1 = time.clock()
# Perform a long process
c = []
for i in xrange(10000000):
    c.append(i)
# Note down end time 
t2 = time.clock()

# Difference is the time taken to complete the long process
print t2-t1


# 
# The datetime module contains functions and classes for working with dates and 
# times, separatley and together.
# 
# Check this link for more information
# http://pymotw.com/2/datetime/index.html#module-datetime

# In[ ]:

import datetime
# Create a Python time object hour=8, minute=30, seconds = 0
t = datetime.time(8,30,0)
print t


# In[ ]:

# Create a Python date object year = 2012, month = 02 and day = 12
print datetime.date(2012,02,12)


# In[ ]:

# Print current date
print datetime.date.today()


# In[ ]:

td = datetime.date.today() # Todays date
tomd = datetime.date.today()+datetime.timedelta(days=1) # Tomorrows date
print td,tomd


# In[ ]:

# If you want both date and time
today = datetime.datetime.today()
print today # ISO style printing


# In[ ]:

'''
In-class activity
Power ball machine creator

A power ball needs a list of 6 numbers.
The first 5 numbers have value between 1 and 59.
The last number also called power ball number will be between 1 and 35

Write a Python program to create this list with 6 numbers. Modify the code
so that it is seeded by the current date. 
'''


# The urllibr module provides an updated API for using internet resources 
# identified by URLs.
# http://pymotw.com/2/urllib2/

# In[ ]:

import urllib2
# Perform a GET method operation
response = urllib2.urlopen('http://www.google.com')
print response.info()


# In[ ]:

# Get a list of functions that are associated with the response object
print dir(response) 


# In[ ]:

for lines in response.readlines():
    print lines.strip()


# The uuid module creates universally unique identifiers for resources in a 
# way that does not require a central registrar. Uuid values are 128 bits long and “can guarantee uniqueness across space and time”. They are useful for identifiers for documents, hosts, application clients, and other situations where a unique value is necessary. The RFC is specifically geared toward creating a Uniform Resource Name namespace.
# 
# Reference:
# http://pymotw.com/2/uuid/index.html#module-uuid.
# 
# The idea is similar to GUID used in Windows programming. The following video 
# (https://www.youtube.com/watch?v=ugqu10JV7dk) traces the
# history of Python in the words of Python creator, Guido van Rossum. The 
# unique identifier similar to one in the url can be 
# created using UUID.

# In[2]:

# getnode() to retrieve the MAC value on a given system:
import uuid
print uuid.getnode()


# In[5]:

# To generate uuid based on the host MAC address,
print uuid.uuid1()


# In[4]:

# Generates an uuid based on random number
print uuid.uuid4() 


# In[ ]:

somerandomstring = 'kdf98234hj23j4y234uy324u234'
print uuid.uuid3(uuid.NAMESPACE_DNS,somerandomstring) # MD5 based hashing
print uuid.uuid5(uuid.NAMESPACE_DNS,somerandomstring) # SHA-1 based hashings


# In[2]:

#import matplotlib libary
import matplotlib.pyplot as plt


#define some data
x = [1,2,3,4]
y = [20, 21, 20.5, 20.8]

#plot data
plt.plot(x, y)

#show plot
plt.show()


# In[9]:

price = [145, 246, 415, 735, 610, 519, 582, 235, 190]
N = len(price)
x = range(N)
width = 1
plt.bar(x, price, width, color = "red")
plt.show()


# In[ ]:

# web scraping example 

from lxml import html
import requests

page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
tree = html.fromstring(page.content)

#This will create a list of buyers:
buyers = tree.xpath('//div[@title="buyer-name"]/text()')
#This will create a list of prices
prices = tree.xpath('//span[@class="item-price"]/text()')

print 'Buyers: ', buyers
print 'Prices: ', prices


# In[ ]:

'''
In-class activity: For the first ten thousand positive integers, 
find the sin(x) for each value with list comprehension and without 
list comprehension. Using the time module, compute 
the time taken by the each method. 
'''

