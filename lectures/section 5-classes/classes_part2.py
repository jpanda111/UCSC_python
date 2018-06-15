
# coding: utf-8

# In this notebook we will discuss the following:
# 
# 1) Operator overloading
# 
# 2) Abstract classes
# 
# 3) class method
# 
# 4) static method
# 
# 5) Proxy design pattern
# 
# 6) Factory design pattern

# Operator overloading: The assignment of more than one function to a 
# particular operator.
# 
# More reading material:
#     
# https://docs.python.org/2/library/operator.html
#     
# http://thepythonguru.com/python-operator-overloading/

# Question - Let us say we have two vectors (5, 8) and (5, -2) and we want to add them. The answer should be (10, 6). Can we use the addition operator '+' to do this?

# In[ ]:

'''
When we try (5, 8) + (5, -2) we get a tuple (5, 8, 5, -2). which is not what 
we were expecting. 
'''
a = (5, 8)
b = (5, -2) 
c = a + b
print c  # here + gives us a new tuple. Which is not our desired result.


# Solution - To perform above vector addition, we need to give a new meaning to the addition operator. For this, we define an \__add\__ method in the class that will automatically get called when instances of the class have to be added using the add, (+) operator. 

# In[ ]:

class Vector(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return 'Vector (%d, %d)' % (self.a, self.b)
   
    def __add__(self,other):
        return Vector(self.a + other.a, self.b + other.b)
    

v1 = Vector(5,8)
v2 = Vector(5,-2)
# when Python interpreter sees + it looks if there is a ___add__ defined in 
# the class and if it, then that method will be used. 
print v1+v2


# Question - How can we notify a class if it fails to implement an important method?
# 
# Solution - how about we have a parent class that raises a flag whenever a method is not impleremented in the child class? This is a reasonable solution. 

# Abstract classes are used to define a signature that will be implemented 
# by all the classes that inherit it. For example, let us say that two 
# programming groups have to read and write into files but how they read and 
# write method may differ. In such cases we can have read and write method 
# signature in the abstract class and the two groups can inherit from the 
# abstract class and create their own concrete classes.
# 
# 
# Below is an example of an abstract class without importing any special 
# module
# 
# Here the abstract class AbstractImage has the methods that consist of 
# signature that all the child classes will inherit. We are raising not 
# implemented error to say that the methods by themselves are not doing 
# anything until implemented by a child class. 

# In[ ]:

class AbstractImage(object):
    def read(self):
        raise NotImplementedError()
    def write(self):
        raise NotImplementedError()

ai = AbstractImage()
print ai
ai.read()


# In[ ]:

class AbstractDicom(object):   
    def read(self):
        raise NotImplementedError()
    def write(self):
        raise NotImplementedError()
    
class Dicom(AbstractDicom):
    def read(self):
        print "reading file in the child class"
        
d = Dicom()
print d
d.read() # Makes the call to Dicom child class


# What will happen if make a call to write() method? 
# 
# d.write() 
# 
# First Python makes the call to Dicom child class. But since 'write' method 
# is not implemented in the child class the write method in the parent class 
# will be called and 'NotImplementedError' will be raised. Let's check.

# In[ ]:

# d.write() 


# In[ ]:

class AbstractDicom(object):
    def read(self):
        raise NotImplementedError()
    def write(self):
        raise NotImplementedError()
    
class Dicom(AbstractDicom):
    def read(self):
        print "reading file"
    def write(self):
        print "writing file"
        
d = Dicom()
print d
d.read() # Makes the call to Dicom child class
d.write() # Makes the call to Dicom child class


# In[ ]:

'''
Create an abstract class called 'InterestCal'. Create a child class called 
'CICal'. The 'CICal' class will inherit the abstract class and implement compound 
interesst calculator. The formula is finalval = P*(1+(r/n)**(years*n))
where n is the number of times the amount is compounded annually.

This child class will have three methods:
1) __init__ method
2) a method called compcal that computes the compound interest 
3) a method called compout that prints the compounded value.


Once all classes have been defined, then call to calculate and print the 
amount. The user should pass the attributes Principal, years, 
interestrate, n when the class is instanstiated. 

Follow the code below:

c = CICal(1000,5,6,2) 
c.compcal()
print c.compout()

In the above code, the principal amount is 1000, the number of years is 5, 
the interest rate is 6%, and n = 2. 
'''


# Abstract base classes can be implemented by using a module called abc. 
# Please check these links to learn more:
# 
# https://pymotw.com/2/abc/
# 
# https://docs.python.org/2/library/abc.html

# Class methods are methods that are bound to the class itself and not 
# to any object(s).  
# Class method takes the class itself as the first argument. 
# 
# syntax for class method
# ```
# @classmethod
# def name_of_the_method(cls):
#     statements
# ```
#  
# Note 1: @classmethod is a decorator. A decorator is a function that takes 
# another function and extends the behavior of the latter function without 
# explicitly modifying it. Decorators provide a simple syntax for calling 
# higher-order functions. The method classmethod takes name_of_the_method as 
# an input and modifies it's behavior.
# 
# Note 2: cls is analogous to self keyword in instance methods. Here cls is 
# a label for the class itself.

# In[ ]:

class Cylinder(object):
    radius = 42
    @classmethod
    def print_radius(cls):
        print "The radius is: ", cls.radius
        # since we want to print the value of radius we have to say 
        # cls.radius or Cylinder.radius
        return True
b = Cylinder.print_radius()
print b

p = Cylinder()
print p.print_radius()


# In[ ]:

import random

class Vector(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    @classmethod
    def createvec(cls):
        return cls(random.randint(1,10), random.randint(1,10))
    
    def __str__(self):
        return 'Vector (%d, %d)' % (self.a, self.b)
   
    def __add__(self,other):
        return Vector(self.a + other.a, self.b + other.b)
    

v1 = Vector.createvec()
v2 = Vector.createvec()
print v1+v2


# Staticmethod doesn't take the class (cls) or self as arguments. It is used 
# to define functions that logically belong to the class and are accessible 
# to all the instances of the class.

# In[ ]:

import math
class Cylinder(object):
    
    @staticmethod
    def youChoose():
        return "We can compute area and volume of the cylinder using methods compArea and compVolume"
    
    def compArea(self, radius):
        Area = math.pi *radius*radius
        return Area
    
    def compVolume(self, radius, height):
        volume = math.pi*radius*radius*height
        return volume

b = Cylinder()
print b.youChoose()

print b.compArea(10)
print b.compVolume(10, 20)


# Accessing a missing attribute:
#     
# When we make a call to an attribute that is not defined for an instance then 
# Python will throw an 'AttributeError'.

# In[ ]:

# An example of accessing a missing attribute
class United(object):
    def __init__(self, name):
        self.name = name
        
u1 = United("Joy")
u1.age


# In[ ]:

# Solution - define the attribute in the class so that we don't get an exception

class United(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
            
u1 = United("Joy", 25)
print u1.name
print u1.age


# Can we safely access attributes that are not defined? Yes, we can by using the magic method \__getattr\__.

# In[ ]:

class United(object):
    def __init__(self, name):
        self.name = name
        
    #def printOut(self):
    #    return "The name is: ", self.name
    
    def __getattr__(self, attr):
        return self.name
    
u2 = United("Joy")
print u2.name
print u2.age
print dir(United)
print u2.printOut


# Design Pattern is a general repeatable solution to a commonly occurring 
# problem in software design. It is a description or template for how to 
# solve a problem that can be used in many different situations.
# https://sourcemaking.com/design_patterns
# 
# Two design patters that we will consider are:
#     Proxy pattern
#     Factory pattern

# Proxy pattern is used when we want to shield access to an object from the
# outside world. For proxy to work, in addition to the class that you want to 
# shield, you also have to create a proxy class, which will internally create 
# an instance of the shielded class when a certain requirement is satisfied 
# or a request is made.
# 
# The syntax for Proxy pattern is 
# ```
# class Proxy:
#     def __init__(self,subject):
#         self.__subject = subject
#     def __getattr__(self,name):
#         return getattr( self.__subject, name )   
# ```

# In[ ]:

# Proxy Pattern is used when an object has to be shielded from its clients.

class Maintenance:
    def visitpage(self):
        print "Our site is under maintenance, please visit us later."
        
class NonMaintenance:
    def visitpage(self):
        print "Welcome to the site"

class Proxy:
    def __init__(self, maintenanceBool):
        if maintenanceBool:
            self.implementation = Maintenance()
        else:
            self.implementation = NonMaintenance()
    def __getattr__(self, name):
        print name, type(name)
        return getattr(self.implementation, name)

MAINTENANCE = True
p = Proxy(MAINTENANCE)
p.visitpage()


# In[ ]:

# Factory pattern

class Menu(object):
    @staticmethod   
    # @staticmethod is an decorator
    def factory(objtype):
        if objtype == 1: 
            return Burger()
        if objtype == 2: 
            return Fries()
        print "Bad menu choice: "
    
class Burger(Menu):
    def listitem(self): print("Burger")

class Fries(Menu):
    def listitem(self): print("Fries")

print "Choose a menu item"
print "1: Burger, 2: Fries"

choice = int(raw_input('Enter your choice number :'))
         
f = Menu.factory(choice)
f.listitem()
print type(f)


# In[ ]:



