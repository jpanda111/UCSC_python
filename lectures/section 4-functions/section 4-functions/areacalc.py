# An example to find area of a triangle using a version of Heron's formula
import math

def calcarea(a,b,c):
	# The three arguments are typecast, as they are initially strings
	Area = area_triangle(a,b,c)
	print "The area is:  %f" % Area
	
	
# Calculate the area 	
def area_triangle(a,b,c):
    A = (1.0/4.0) * math.sqrt(
        2*(a**2 * b**2 + a**2 * c**2 + b**2 * c**2) -
        (a**4 + b**4 + c**4) )
    return A
 
if __name__=='__main__': # more obvious way to start: same as main function in C
# if don't belong to any module, python will think it belong to main module
	#The arguments come from the user
	a = float(raw_input('Enter the value for the first side: '))
	b = float(raw_input('Enter the value for the second side: '))
	c = float(raw_input('Enter the value for the third side: '))
	calcarea(a,b,c)  

