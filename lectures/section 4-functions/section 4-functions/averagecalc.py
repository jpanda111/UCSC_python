# An example for taking command line input
# sys.argv is the list of command line parameters
import sys
# raw_input is taking command from python command line; but sys is taking command from os sys;

def calcaverage(x,y):
    Average = (x+y)/2
    print "The average of %0.2f and %0.2f is:  %0.2f" %(x,y,Average)
    return Average
	
if __name__=='__main__':
    #The command line arguments come into the program as a list of string
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    print sys.argv
    # if we do: python averagecalc.py 10 20, you will get sys.argv as following: ['averagecalc.py','10','20']
    calcaverage(x,y)  
