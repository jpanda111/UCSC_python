
# coding: utf-8

# A regular expression is a text matching pattern that is described in a 
# specialized syntax. The pattern has instructions, which are executed with a 
# string as an input to produce a matching subset. The Python module to perform 
# regular expression is re. Typically, re is used to match or find strings.
# 
# Visit the following sites to learn more
# 
# http://pymotw.com/2/re/
#     
# http://www.thegeekstuff.com/2014/07/python-regex-examples/
#     
# http://www.diveintopython.net/regular_expressions/
#     
# https://docs.python.org/2/library/re.html

# In[6]:

import re


# In[2]:

patterns = 'and'
text = 'Python is a dynamically typed language and also has a simple syntax'
print re.search(patterns, text)
if re.search(patterns, text):
    print 'There is a match'
else:
    print 'Found no match'


# In[ ]:

patterns = 'or'
text = 'Python is a dynamically typed language and also has a simple syntax'
print re.search(patterns, text)
if re.search(patterns, text):
    print 'There is a match'
else:
    print 'Found no match'


# In[ ]:

patterns = ['and', 'or']
text = 'Python is a dynamically typed language and also has a simple syntax'

for pattern in patterns:
    print 'Trying to find a match for "%s" in "%s" - ' %(pattern,text)
    
    if re.search(pattern, text):
        print 'There is a match'
    else:
        print 'Found no match'


# In[ ]:

pattern = 'and'
text = 'Python is a dynamically typed language and also has a simple syntax'

compare = re.search(pattern,text)

s = compare.start() # start() returns the starting position of the match
e = compare.end() # end() returns the ending position of the match

print 'Found "%s" in "%s"  from %d to %d ' %(pattern,text,s,e)


# In[ ]:

mynumber = 1034567810378103
pattern = 10
mynumber_str = str(mynumber)
pattern_str = str(pattern)
# findall() function finds all the substrings of the input that match the 
# pattern without overlapping syntax re.findall(pattern, string)
print re.findall(pattern_str,mynumber_str)
count = len(re.findall(pattern_str,mynumber_str))
print 'In the given text, %d occured  %d times' %(pattern, count)


# In[ ]:

# finditer() returns an iterator that produces match instances instead of the 
# strings returned by findall
# syntax re.finditer(pattern, string)

text = '1034567810378103'
pattern = '78'
count = 0
print re.finditer(pattern,text)
for match in re.finditer(pattern,text):
    s = match.start() 
    e = match.end() 
    count = count + 1
    print 'The pattern "%s" starts at %d and ends at %d ' %(pattern, s, e)
print 'In the given text, "%s" occured  %d times' %(pattern, count)


# The group() returns the substring that was matched by the re. Adding groups 
# to a pattern lets you isolate parts of the matching text, expanding those
# capabilites to create a parser. 

# In[ ]:

strval1 = 'Barack Obama, Michelle Obama, Joe Biden, Jill Biden'
list1 = strval1.split(',')
print list1

for items in list1:
    firstname = re.match(r'(.*)Obama',items)
    if firstname:
        # command below returns every element in the list 
        # that has Obama in it
        print firstname.group(0) 
        
        # command below returns first name of the element in the 
        # list that has Obama in it
        print firstname.group(1) 
        


# In[ ]:

strval = 'San Francisco, San Jose, San Carlos, Sunnyvale, Cupertino'
strval_list = strval.strip().split(',') # converting strval into a list

b = []
for items in strval_list:
    allnames = re.match(r'San(.*)', items.strip()) 
    # returns a subset of the list which starts with San 
    if allnames:
        b.append(allnames.group(1))
print b


# re.compile() function is used to compile pattern into pattern objects, 
# which have methods for various operations such as searching for pattern 
# matches or performing string substitutions. 
# syntax:
# ```
# re.compile(pattern)
# ```

# In[ ]:

strval = 'San Francisco, San Jose, San Carlos, Sunnyvale, Cupertino'
rec = re.compile('San')
print re.findall(rec,strval)


# In[ ]:

# Returns an iterator
for items in re.finditer(rec,strval):
    print items


# In[ ]:

# Returns an iterator
for items in re.finditer(rec,strval):
    print items.start(),items.end()


# First method to find and replace:
# 
# The replace() function will replace substrings.
# 
# syntax 
# ```
# input_text.replace('pattern', 'replacement') 
# ```

# In[ ]:

a = strval.replace('San','S.')
print strval
print a


# Second method to find and replace:
#     
# The re.sub() function can be used to replace substrings.
# 
# syntax
# ```
# re.sub(pattern, replacement, string) 
# ```

# In[ ]:

strval1 = re.sub('San','S.',strval)
print strval1


# In[ ]:

t = 'It\'s a dog\n'
print t

t = r'It\'s a dog\n'
print t


# Cheat sheet for re
# 
# \w - Matches characters from A-Z, a-z, 0-9 or _ also writen as A-Za-z0-9_
# \W - Matches nonword characters.
# \s - Matches whitespace. Equivalent to [ \t\n\r\f].
# \S - Matches nonwhitespace.
# \d - Matches digits. Equivalent to [0-9].
# \D - Matches nondigits.
# ^ start of string, or line
# \A  Start of string
# \b  Match empty string at word (\w+) boundary
# \B  Match empty string not at word boundary
# \Z  End of string
# 
# {m}     Exactly m repetitions
# {m,n}   From m (default 0) to n (default infinity)
# *       0 or more. Same as {,}
# +       1 or more. Same as {1,}
# ?       0 or 1. Same as {,1}
# 
# Reference 
# https://github.com/tartley/python-regex-cheatsheet/blob/master/cheatsheet.rst

# In[ ]:

# in this example we want to make sure that the user enters valid email address
import re

ymail_check = re.compile(r'(\w+@\w+\.(com|net|org|edu))')
while True:
    ymail = raw_input ("Please, enter your email: ")
    if ymail_check.search(ymail):
        print 'you entered a valid email'
        breaks
    else:
        print "Please enter your email correctly!"


# In[ ]:

# The re.search() method takes a regular expression pattern and a string and
# searches for that pattern within the string. 
# The syntax is re.search(pattern, string)
import re
name = 'Roosovelt, Eleanor'
a = re.search('(\w+), (\w+)',name)
# (\w+) matches multiple occurrances of A-Za-z0-9_
print a.group(0)
print a.group(1)
print a.group(2)


# In[4]:

name = 'Roosovelt, Eleanor'
a = re.search('(?P<lastname>\w+), (?P<firstname>\w+)',name)
'''
?P<lastname>\w+ finds pattern that has characters A-Za-z0-9_ and assigns 
it to lastname
'''

print a.group(0)
print a.group('lastname')
print a.group('firstname')


# In[ ]:

# There is only one space after , 
strval = 'Elizabeth Warren, 65'
a = re.search('(?P<firstname>\w+) (?P<lastname>\w+), (?P<age>\d+)',strval)
print a.group(1)
#print a.group('age')


# In[ ]:

# What happens if there are more spaces after , ? 
strval = 'Elizabeth Warren,           65'
a = re.search('(?P<firstname>\w+) (?P<lastname>\w+), \s+(?P<age>\d+)',strval)
print a#.group(0)
print a.group('age')


# In[ ]:

'''
In-class activity: In the below paragraph, find the number of occurances of 
words - of, the and food.

Coral reefs are some of the most biologically rich and economically valuable 
ecosystems on Earth. They provide food, jobs, income, and protection to 
billions of people worldwide. However, coral reefs and the magnificent creatures 
that call them home are in danger of disappearing if actions are not taken 
to protect them. They are threatened by an increasing range of impacts including 
pollution, invasive species, diseases, bleaching, and global climate change. 

The rapid decline and loss of these valuable, ancient, and complex ecosystems 
have significant social, economic, and environmental consequences in the 
United States and around the world.
'''


# In[ ]:

'''
In-class activity: 
In the below paragraph, there are typos. The spelling mistakes are in the 
words: tping, componts, programy and binare. Create a dictionary with the key 
being the incorrect word and the value is the correct word. Then replace the 
incorrect word with the correct word and print the corrected text.

'''

myText = '''Python is an interpreted, object-oriented, high-level programming 
language with dynamic semantics. Its high-level built in data structures, 
combined with dynamic tping and dynamic binding, make it very attractive for 
Rapid Application Development, as well as for use as a scripting or glue 
language to connect existing componts together. Python's simple, easy to learn 
syntax emphasizes readability and therefore reduces the cost of program 
maintenance. Python supports modules and packages, which encourages programy 
modularity and code reuse. The Python interpreter and the extensive standard 
library are available in source or binare form without charge for all major 
platforms, and can be freely distributed.'''


# In[12]:

# extracting year from a text file using regex
import re
pattern = re.compile("(\d+)")

for i, line in enumerate(open('modify.txt')):
   #print i, line, re.finditer(pattern, line)
   for m in re.finditer(pattern, line):
       year = m.group(1)
       print  'The year is ', year


# In[ ]:

# extracting data from a text file using regex
import re

parts = [
    r'(?P<host>\S+)',                   # host %h
    r'\S+',                             # indent %l (unused)
    r'(?P<user>\S+)',                   # user %u
    r'\[(?P<time>.+)\]',                # time %t
    r'"(?P<request>.+)"',               # request "%r"
    r'(?P<status>[0-9]+)',              # status %>s
    r'(?P<size>\S+)',                   # size %b (careful, can be '-')
]
pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')
status1 = []

fo = open("apache50log.txt")
for line in fo.readlines():
    m = pattern.match(line)
    res = m.groupdict()
    print res
    status1.append(res['status'])

print status1
statusdict = {}
statusset = set(status1)
for item in statusset:
    statusdict[item] = status1.count(item)
    
print statusdict


# In[ ]:



