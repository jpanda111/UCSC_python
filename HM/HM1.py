'''
Question 1: 5points

Use the formula

Pn = P0*(1+r)^n

where P0 is the principal amount, Pn is the compounded principal, 
r is the rate of interest and n is the number of year.

Assume r = 10% and n = 1 to 20, create a Python list that will store 
the value of (1+r)^n where n = 1 to 20. Subsequently, take an input from 
the command line for the value of P0 and calculate Pn all values of n. 
Repeat this process until a 'Q' or 'q' is pressed to quit the program.

'''
r = 0.1
l = []
# store the value of (1+r)^n
l = [(1+r)**x for x in range(21)]
l = l[1:]
# take input from command line
P0 = raw_input("Enter the principal amount:")
# repeat the process until a 'Q' or 'q' is pressed to quit
while P0.lower() != 'q':
    Pn = []
    for item in l:
        Pn.append(float(P0) * item)
    P0 = raw_input("Enter the principal amount or quit (enter Q or q):")
    