import file3

a = 10.0
b = 0
w = (0,0,)

try:
    w = file3.inv(a,b)
except ZeroDivisionError:
    print "Could not complete inv()"
file3.insum(w[0],w[1])
