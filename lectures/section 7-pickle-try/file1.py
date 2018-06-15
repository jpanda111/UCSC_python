def inv(a,b):
    c = 0
    d = 0
    try:
        c = 1.0/a
        d = 1.0/b

    except ZeroDivisionError:
        raise ZeroDivisionError("One or more numbers is zero.") 
    return (c,d)

def insum(c,d):
    e = c + d
    return e

