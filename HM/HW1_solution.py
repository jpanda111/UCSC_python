'''
Question 1

Use the formula

Pn = P0*(1+r)^n

where P0 is the principal amount, Pn is the compounded principal,  
r is the rate of interest and n is the number of year.

Assume r = 10% and n = 1 to 20, create a Python list that will store 
the value of (1+r)^n where n = 1 to 20.  Subsequently, take an input from 
the command line for the value of P0 and calculate Pn all values of n.  
Repeat this process until a special key is used to quit the program. 
'''
r = 10/100.0 # Divide by float, to avoid integer division
n = range(1, 20)
nr = [pow(1+r, i) for i in n]
print nr
while True:
    P0 = raw_input('Enter the initial principal: ')
    if P0.lower() == 'q':
        break
    P0 = float(P0)
    P = [P0*i for i in nr]
    print P
	
	
'''
Question 2
https://en.wikipedia.org/wiki/Run-length_encoding

Implement an encoding scheme.

A string 
WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW 
has 67 characters. Write a Python program 
with a function called getcompressed to convert this string to 
12W1B12W3B24W1B14W. The new string is created
by calculating the number of times a characters appears consecutively and
placing the character next to it. The new string only needs 18 character,
thus compressing the original string by 73%.
'''

orig_string = 'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'

def getcompressedstring(inputstring):
    firstitem = orig_string[0]
    #print firstitem
    count = 0
    finalstring = []
    for i in range(len(orig_string)-1):
        if orig_string[i] == firstitem:
            count = count+1 
        else:
            newstring = '%d%s'%(count,firstitem)
            finalstring.append(newstring)
            firstitem = orig_string[i]
            #print newstring, firstitem
            count = 1
    
    count = count+1 
    newstring = '%d%s'%(count,firstitem)
    finalstring.append(newstring)
    return ''.join(finalstring)

print getcompressedstring(orig_string)