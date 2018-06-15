
# coding: utf-8

# In this notebook we will discuss:
# 1. File IO
# 
#     a. using module csv
#     
#     b. using module xlrd
#     
# 2. walking a directory and all its sub-directories
# 
#     a. glob
#     
#     b. os 
#     
# 3. creating custom modules

# In[ ]:

import csv
with open('exgrade.csv', 'r') as fo:
    alllines = csv.reader(fo,delimiter=',')
    for lines in alllines:
        print lines


# In[ ]:

import csv
with open('animals.csv', 'w') as fo:
    wo = csv.writer(fo)
    lines = [['Zebra', 10], ['Giraffe', 17]]
    wo.writerows(lines)


# In[ ]:

import csv
with open('animals.csv', 'r') as fo:
    alllines = csv.reader(fo,delimiter=',')
    for lines in alllines:
        print lines


# Module xlrd is used for reading data from xls and xlsx files.
# 
# To learn more check the following links:
# 
# http://www.python-excel.org/
# 
# http://www.youlikeprogramming.com/2012/03/examples-reading-excel-xls-documents-using-pythons-xlrd/

# In[5]:

# Open an excel file and get all the sheet names
import xlrd
wb = xlrd.open_workbook('exgrade.xls')
print wb.sheet_names()


# In[6]:

# In sheet 1, get the number of rows
ws = wb.sheet_by_name('Sheet1')
print ws.nrows


# In[ ]:

print ws.row(0) # Get the content of first row as a list
print ws.row(0)[1] # Get the second element of the first row list 


# Module xlwt is used to write data to xls files. 

# In[8]:

# xlwt module is used to write into excel file.
import xlwt
workbook = xlwt.Workbook() 
sheet = workbook.add_sheet("Sheet 1") 

#sheet.write(0, 0, 'Adam') # row, column, value

g = [['Name', 'Security code'], 
     ['Adam', ' 10034'],
     ['Nitin', ' 10043'],
     ['Rob', ' 10134'],
     ['Sheela', ' 10045']]

for i,v in enumerate(g):
    print i, v, len(v)
    if len(v) >= 2:
        sheet.write(i,0,v[0])
        sheet.write(i,1,v[1])
        
workbook.save('Xcel1.xls')


# Module sqlite3 is used to write data to and read data from databases.

# In[ ]:

import sqlite3

# Create a connection to sqlite
conn = sqlite3.connect('test.db')

# Open a cursor
c = conn.cursor()

# Execute any SQL statement
# Create table named "stocks" if it does not already exist.
c.execute("create table if not exists stocks            (date text, trans text,symbol text, qty real, price real)")

# Add entries
c.execute("insert into stocks values ('2006-02-05','SELL','RHAT',50,50.25)")
c.execute("insert into stocks values ('2006-03-15','BUY','GOOG',1000,350.13)")
c.execute("insert into stocks values ('2006-10-05','BUY','GOOG',100000,400.14)")
conn.commit()

# Query all the entries in the database
alllines = c.execute("select * from stocks")
print alllines

# Print it
for lines in alllines:
    print lines

c.close()


# In[ ]:

'''
In-class activity - Create a database and call it 'UserSignUp.' In the 
database create a table called 'FirstSignUp' with columns Name, Country, 
Date, Type. Date should contain information on first login date and type 
should be paid or free user. Add five entries. Then print out the rows. 
'''


# Module os provides operating system dependent functionalities. 
# 
# https://docs.python.org/2/library/os.html

# In[11]:

import os
# gives a list of folders and files that are in 
# the current working directory
os.listdir(".")


# Module glob can be used to finds all the pathnames matching a specified 
# pattern according to the rules used by the Unix shell.
# 
# glob.glob(_directory_name) will return all the files in a particular 
# directory or folder

# In[13]:

import glob

# will return a list of files that are in the current working directory 
print glob.glob("*.*")


# In[ ]:

# in this example it will return all the ipython notebook files in the 
# current directory
print glob.glob("*.ipynb")


# In[ ]:

import os
# os.walk returns three values - root, directories and files and they are 
# passed to the variables root, dirs and files respectively.
for root, dirs, files in os.walk("sridevi/Desktop/"):
    # root, dirs, files
    for file in files:
        if file.endswith(".py"):
             print os.path.join(root, file)


# In[ ]:

import os
os.getcwd()


# Different ways of importing a module.

# In[ ]:

# Import all functions in a given module.
# We have to refer to the module name when 
# calling the function
import math
print math.sin(math.pi/4)


# In[ ]:

# Import all functions in a given module.
# We do not need to refer to the module name when 
# calling the function
from math import *
print sin(pi/4)


# In[ ]:

# Give a shortcut name to the module. 
# Especially true for modules with long names such as matplotlib
import math as ma
print ma.sin(ma.pi/4)


# In[ ]:

# Only import the necessary functions from a module
# This is memory efficient
from math import sin,pi
print sin(pi/4)


# In[ ]:

import numpy as np
a = np.array([1,5,8,6], float)
print a
c = a/2
print c


# In[ ]:

print a.sum()
print a.prod()
print a.min()
print a.max()


# Subprocess module is useful for making calls to the *nix operating system. 
# Check documentation in https://docs.python.org/2/library/subprocess.html
# https://pymotw.com/2/subprocess/

# In[ ]:

'''
You need to use the Popen function and pass the command
The following piece of code can only be used on Mac or Linux. 

Invoking the system shell with shell = True can be a security hazard if 
combined with untrusted input
'''

import subprocess
sp = subprocess.Popen('ls', stdout=subprocess.PIPE)
s = sp.communicate() # Returns a tuple (stdout,stderr)
print s

# You can iterate through the tuple that is returned by the function
for items in s:
    print items


# In[15]:

'''
The following subprocess code can be used on Windows
'''
import subprocess
sp = subprocess.Popen('dir', shell =True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#s = sp.communicate() # Returns a tuple (stdout,stderr)

results = []
# You can iterate through the tuple that is returned by the function
for items in sp.stdout:
    results.append(items)
    
print results


# Creating custom modules

# In[ ]:

# The file prog1.py is in the same folder as this IPython notebook
import prog1
print prog1.increment(2,3)


# In[ ]:

# The file uprog1.py is in the folder "ufolder" which is 
# in the same location as this IPython notebook
from ufolder import uprog1
print uprog1.increment(10)


# In[ ]:

import ufolder
print ufolder.uprog1.increment(16)


# In[ ]:

import ufolder as uf
print uf.uprog1.increment(20,3)


# Note: sometimes Jupyter (iPython) notebook might give an attribute error when you say - 
# import usermodule_name. 
# 
# the best way to go around this is to say - 
# from usermodule_name import userfile_name

# In[ ]:

'''
In-class activity - create a folder and make it a Python importable folder. 
Write a program that returns a list of odd numbers from a given list and 
save it in that folder. Write a code in the iPython notebook that imports 
the folder and then make a function call and supply the list.
'''

