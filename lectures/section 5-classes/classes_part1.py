
# coding: utf-8

# In this notebook we will dicuss:
# 
# 1) Object Oriented Programming - OOPS
# 
# 2) class variables
# 
# 3) instance methods and instance variables
# 
# 4) parent and derived classes by inheritance

# To keep syntax simple, Python's classes implements functionality as 
# needed to perform the task. It has all functionality that you find in 
# object-oriented programming systems (OOPS) such as inheritance 
# (from single and multiple base classes), method over-riding etc. 
# Unlike C++, programmer does not have to explicitily destroy objects.  
# They are removed dynamically by the Garbage Collector.
# 
# All class members are public by default. Private variables are created by 
# using __ such as __filename.  
# 
# One can also create a "C" style struct that contains only values but 
# no function
# 
# More reading material:
#     
# http://www.tutorialspoint.com/python/python_classes_objects.htm
# 
# http://www.jeffknupp.com/blog/2014/06/18/improve-your-python-python
# -classes-and-object-oriented-programming/
# 

# In this section, we will learn various terminologies such as Class, 
# Class variable, Data member, function overloading, instance variable, 
# inheritance, instance, method, object, operator overloading. 
# Here is an explanation: 
# 
# Class: In object-oriented programming, a class is an extensible 
# program-code-template for creating objects, providing initial values for 
# state (member variables) and implementations of behavior 
# (member functions or methods)  - Wikipedia
# The class is the definition of the functionality that is programmed. 
# 
# Class variable: A variable that is shared by all instances of a class. 
# Class variables are defined within a class but outside any of the 
# class's methods. Class variables are not used as frequently as 
# instance variables are.
# 
# Instance variable: A variable that is defined inside a method and 
# belongs only to the current instance of a class.
# 
# Inheritance: The transfer of characteristics of a class to other 
# classes that are derived from it.
# 
# Instance: An individual object of a certain class. An object obj 
# that belongs to a class Circle, for example, is an instance of the 
# class Circle.
# 
# Instantiation: The creation of an instance of a class.
# 
# Object :  The programmer has to create an instance of the class known as
# object/instance in order to use the functionality. The member variables 
# specific to the object/instance are called instance variables. 
# The member variables that are accessible across various instances of 
# a class are called class variables. 
# 
# Operator overloading: The assignment of more than one function to a 
# particular operator.
# 

# Syntax for class
# 
# 
# class class_name(object):
# 
#     '''Documentation for the class should be put here'''
#     
#     define all the methods and instance variables
#     
# A function inside a class is called a method.
# A class can have many methods and many instance/class variables 
# or attributes.

# In[ ]:

'''
Variables such as name and balance are usable by more than one methods. 
Their values are also specific to that instance.
Hence they need to be instance variable.
'''
class Customer(object):
    
    '''The attributes for this class are name and balance '''
    
    def __init__(self,name):
        self.name = name
        self.balance = 0.0
        
    # you must explicitly list self as the first argument for each method
    # including __init__ method
        
    # withdraw is a method    
    def withdraw(self, amount):
        self.balance -=amount
        return self.balance
    
    # deposit is a method
    def deposit(self, amount):
        self.balance +=amount
        return self.balance
        
# creating an instance of the class named Customer  
b = Customer("Leo")  
print b.deposit(2000) # calling deposit method and passing a value
print b.withdraw(500) # calling withdraw method and passing a value
print "Customer name %s and balance %0.2f "%(b.name, b.balance)


# ```__init__``` method is called immediately after an instance of the 
# class is created.

# Method overloading: The assignment of more than one behavior 
# to a particular method. The operation performed varies by the types 
# of objects or arguments involved.

# In[1]:

# A class with multiple initalizers
class Customer(object):
    def __init__(self,name, balance=None):
        self.name = name
        if balance is None:
            balance = 0.0
            
        self.balance = balance 
    
    def withdraw(self, amount):
        self.balance -=amount
        return self.balance
    
    def deposit(self, amount):
        self.balance +=amount
        return self.balance
        

# creating an instance of the class named Customer. The instance is called b.
b = Customer("Leo",10000) 
print b
b.withdraw(500) # calling withdraw method and passing a value
b.deposit(2000) # calling deposit method and passing a value
print "Customer name %s and balance %0.2f "%(b.name, b.balance)

# Try calling 
b = Customer("Euler")
print "Customer name %s and balance %0.2f "%(b.name, b.balance)


# In[ ]:

# creating another object for class Customer
c = Customer("John")
c.withdraw(325)
c.deposit(675)
print "Customer name %s and balance %0.2f "%(c.name, c.balance)


# Private Instance Variables are created by using __ (double underscore) 
# before the instance variable will make the variable private for the class.
# 
# In Python there are no true private or protected variables or methods. 
# Private instance variables and methods are used mostly for internal 
# purposes or to avoid namespace clashes.  

# In[ ]:

# An example of class with private variable
class Customer(object):    
    def __init__(self,name):
        self.name = name
        self.__balance = 0.0 
        
    def withdraw(self, amount):
        self.__balance -=amount
        return self.__balance
    
    def deposit(self, amount):
        self.__balance +=amount
        return self.__balance
        
    def get_balance(self):
        return self.__balance
    
b = Customer("Leo")  
b.withdraw(500)
b.deposit(2000)
print b.get_balance()
#print b.__balance # this will fail as __balance is a private variable 


# In[ ]:

'''
In-class activity - To the Customer class, add a method 
called promotion. Ask the user if they want to know about promotional 
offers. Depending on their choice, show them the offer or say thank you.
'''


# Important things to remember when you are defining a class:
#     
# 1) class class_name(object):
# 
# 2) it is ideal to have an \__init\__ method with attributes.
# 
# 3) self should be the first attribute in all the methods, 
#    including \__init\__
#    
# 4) in the \__init\__ method assign the instance attributes to 
#    self.attribute_name. Use self.attribute_name for all subsequent 
#    operations.

# Private Methods - are created by using double underscore before the method  name when the method is defined. 

# In[ ]:

class Class1:
    def outside(self):
        print "This is a public method"
        
    # __inside is a private method
    def __inside(self):
        print "This is a private method"
        
p = Class1()
p.outside() # this will work
#p.__inside() # this will not work as we are calling a private method


# The dir method gives a list of all the methods in a class including 
# private methods (albeit with a weird naming convention).

# In[2]:

print dir(Class1) 


# Roundabout way of accessing private methods.
# 
# The following construct will allow us to call a private method
# 
# instance._classname_privatemethod()

# In[ ]:

p._Class1__inside()


# In[ ]:

# We can use instance variables inside the private method just 
# as you would for public methods
class Class1(object):
    def outside(self):
        print "This is a public method"
        self.somevar = 10
        
    def __inside(self):
        self.somevar = 20
        print "This is a private method"
        
p = Class1()
p.outside() 
p.somevar


# If we cannot call the private method, how do we use it?
# 
# Private methods have to be called in a public method inside a class 
# definition. Below we are calling __private method 
# inside public method

# In[3]:

class Class1(object):
    def outside(self):
        print "Inside public method"
        self.somevar = 10
        print "somevar value before calling private method ",self.somevar
        self.__inside()
        
    # To create a private method, prefix __ (double underscore) to the 
    # method name
    def __inside(self):
        print "Inside private method"
        self.somevar = 20
        
p = Class1()
p.outside() 
p.somevar


# More about private methods and variables can be read at the following links:
# 
# http://stackoverflow.com/questions/70528/why-are-pythons-private-
# methods-not-actually-private
# 
# http://effbot.org/pyfaq/tutor-how-do-i-make-public-and-private-attributes-
# and-methods-in-my-classes.htm

# Class variable: A variable that is shared across all 
# instances of a class. Class variables are defined within a class but 
# outside any of the class's methods. Class variables are not used as 
# frequently as instance variables.

# In[4]:

class Employee(object):
    empCount = 0 #Class variable. No self. prefix
    className = 'Employee' #Class variable. No self. prefix
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empCount +=1
        
    def displayCount(self):
        print "Total Employee %d" %Employee.empCount
    
    def displayEmployee(self):
        print "Name:   ", self.name,  ", Salary:   ", self.salary
        
emp1 = Employee("Tara", 20000)
emp2 = Employee("Zeera", 7000)
emp3 = Employee("Cara", 5000)
emp4 = Employee("John",4000)
emp2.displayEmployee()
emp2.displayCount()
#print "Total Employee %d" % Employee.empCount

if(emp2.className == 'Employee'):
    print "I have a Employee class"


# In[ ]:

# Example of documentation in a class
class SaveWater:
    ''' This is a documentation of SaveWater'''    
    def __init__(self,statename):
        self.statename = statename
        if self.statename.lower() == "california":
            print "Use less water!"
        else:
            print "Still use less water!"
        
statename = raw_input("Please enter name of your state ")
s = SaveWater(statename)


# In[ ]:

print s.__doc__


# In[ ]:

''' C style struct that has class variables but no methods '''

class Person(object):
    pass

# Create an instance of Person class.  This is called object
leo = Person()
# we are giving class attributes here and there are no methods
leo.name = 'Leo Euler' 
leo.zipcode = '95117'
leo.ssn = '123-45-6789'

print leo
print leo.name, leo.zipcode, leo.ssn
print leo.__dict__


# Built-in class attributes:
# 
# ```__dict__``` : Dictionary containing the class's namespace.
# 
# ```__doc__``` : Class documentation string or None if undefined.
# 
# ```__name__```: Class name.
# 
# ```__module__```: Module name in which the class is defined. This attribute is 
# ```__main__``` in interactive mode.
# 
# ```__bases__``` : A possibly empty tuple containing the base classes, in the 
# order of their occurrence in the base class list.

# In[8]:

class Class1:  
    def __init__(self,name):
        self.name = name
    def listname(self):
        return self.name
    def setname(self,name):
        self.name = name

obj1 = Class1('Ravi')
print obj1.listname()
print obj1, type(obj1)

print obj1.__dict__
print Class1.__doc__
print Class1.__module__
print Class1.__bases__


# hasattr() can be used to check if an instance has a specific attribute. This returns True or False
# 
# Syntax for hasattr:
# 
# hasattr(instance_name, attribute_name)

# In[9]:

hasattr(obj1, 'name')    # Returns true if 'name' attribute exists


# getattr() is used to obtain value of a specific attribute for an instance.
# 
# Syntax for getattr
# 
# getattr(instance_name, attribute_name)

# In[ ]:

print getattr(obj1, 'name')    # Returns value of 'name' for obj1


# The following command can also be used to obtain the value of an attribute
# in an instance
# 
# instance_name.attribute_name

# In[ ]:

# this is same as getattr(obj1, name)
print obj1.name 


# Below, we are resetting an attribute value without using any special 
# functions.

# In[ ]:

obj1.name = 'Robbie'
print obj1.name


# setattr() can be used to reset an attribute value
# 
# Syntax for setattr:
# 
# setattr(instance_name, attribute_name, new_value)

# In[ ]:

setattr(obj1, 'name', 'Robbie') # Set attribute 'name' to Robbie


# Deleting objects
# 
# Deletion happens via Garbage collection.  One can also delete objects 
# and its variables using``` __del__``` method.
# 
# 
# There are two ways to delete an object.  You do not have to use either,
# instead you let Python do garbage collection.

# In[ ]:

class Class1(object):  
    def __init__(self,name):
        self.name = name
    def listname(self):
        return self.name
    # the following method is executed during object deletion 
    def __del__(self):
        print self.name,"destroyed"
obj1 = Class1('Darth Vader')

# first method
del obj1
obj1.name
# second method
#obj1 =  None
#print obj1


# In[ ]:

class Class1(object):  
    def __init__(self,name):
        self.name = name # this is a instance variable
    def listname(self):
        return self.name
    def __del__(self):
        print self.name,"destroyed"
    # in the following method, a string is returned whenever the print 
    # is called with the object as input
    def __str__(self):
        return "The name is %s " %self.name
    
obj1 = Class1('Darth Vader')
# This will call __str__ method, thus enabling a pretty printing of object
print obj1 
del obj1


# Note: ```__del__``` and ```__str__``` are special methods that are defined by Python. 
# Hence, they have a double underscore before and after del and str 
# respectively.

# Class Inheritance - The transfer of the characteristics of a class to 
# other classes that are derived from it.

# In[ ]:

# An example of an inherited class
class Animal(object):
    def say_something(self):
        return "I'm an animal!"
    
'''
Here Cat and Dog are child classes that are inheriting from Animal. 
The child class, say_something method overrides the behavior 
of the say_something of the parent class. This is called method overriding. 
'''

class Cat(Animal):
    def say_something(self):
        return "Meow"
    
class Dog(Animal):
    def say_something(self):
        return "Bow-wow"
    
a = Animal()
print a.say_something()
d = Dog()
print d.say_something()
c = Cat()
print c.say_something()


# Sometimes you will have to call both the child class method and also the
# parent class (also called super class) method. You can do so by using 
# super method.

# In[ ]:

class Animal(object): 
    def say_something(self):
        return "I'm an animal!"
    
#child class or derived class
class Cat(Animal):
    def say_something(self):
        # super(child_class_name,self).methodname()
        # here methodname() should be the method that 
        # you want to call from the parent class
        s = super(Cat,self).say_something()
        return "%s - %s" %(s, "Meow")
    
class Dog(Animal):
    def say_something(self):
        s = super(Dog,self).say_something()
        return "%s - %s" %(s, "Bow-wow")
c = Cat()
print c.say_something()
d = Dog()
print d.say_something()


# In[ ]:

print Dog.__bases__ # Prints the list of base classes


# In[ ]:

# The name attribute in this class is a class variable.  
# We will use this as a super class for the next cell.
class Animal(object):
    name = 'Animal'
    def eat(self):
        print "Animal eating"
    def drink(self):
        print 'Animal drinking'
a = Animal()        
b = Animal()
print a.name, b.name


# In[ ]:

# Method overloading in the same class. 
# Only the last method definition is used.
class Animal(object):
    name = 'Animal'
    def eat(self):
        print "Animal eating"
      
    def drink(self,name):
        print 'Animal %s drinking'%(name)
        
    def drink(self, name = 'Dog'):
        print 'Latest method - Animal %s drinking: '%(name)

        
a = Animal()        
a.drink()
b = Animal()
b.drink('Cow')


# In[ ]:

# Method overriding between child and parent class.
class Animal(object):
    name = 'Animal' # class variable
    def eat(self):
        print "Animal eating"
    def drink(self):
        print 'Animal drinking'
        
class Dog(Animal):
    name = 'Dog' # class variable
    def eat(self): 
        print "Dog eating"
        
d = Dog()
d.eat()
print d.name
d.drink()


# In[ ]:

# Method overriding
class Animal(object):
    name = 'Animal' # class variable
    def eat(self):
        print "Animal eating"
    def drink(self):
        print 'Animal drinking'
        
class Dog(Animal):
    name = 'Dog' # class variable
    def eat(self): 
        print "Dog eating"
    def drink1(self):
        print 'Dog drinking'
    
        
d = Dog()
d.eat()
print d.name
d.drink()
d.drink1()


# In[ ]:

# multiple inheritance.  A child can have multiple parents.
class Organism(object):
    name = 'Organism'
    def eat(self):
        print 'Organism eating'
    def drink(self):
        print 'Organism drinking'
        
class Animal(object):
    name = 'Animal'
    def eat(self):        
        print "Animal eating"
           
class Dog(Organism,Animal):
    #name = 'Dog'
    def eat(self):
        print "Dog eating"
        
d = Dog()
d.eat()
print d.name
d.drink()


# In[ ]:

# multiple inheritance
'''
When two parents have same method(s) then the method in the left most 
parent of the child class will be executed.
'''

class Organism(object):
    name = 'Organism'
    def eat(self):
        print 'Organism eating'
    def drink(self):
        print 'Organism drinking'
        
class Animal(object):
    name = 'Animal'
    def eat(self):        
        print "Animal eating"
    def drink(self):
        print 'Animal drinking'
 

class Dog(Animal,Organism):
    name = 'Dog'
    def eat(self):
        print "Dog eating"
        
d = Dog()
d.eat()
print d.name
d.drink()


# Diamond problem - 
# 
# Multi level Mutiple inheritance 
# 
# http://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with
# -multiple-inheritance
# 
# http://en.wikipedia.org/wiki/Multiple_inheritance#The_diamond_problem
#    

# In[19]:

class LivingBeing(object):
    name = 'Living Being'
    def drink(self):
        print "Living being drinking"
    def eat(self):
        print "Living being eating"

class Organism(LivingBeing):
    name = 'Organism'
    #def eat(self):
    #    print 'Organism eating'
        
class Animal(LivingBeing):
    name = 'Animal'
    def eat(self):        
        print "Animal eating"
    def drink(self):
        print 'Animal drinking'
        

class Dog(Organism, Animal):
    name = 'Dog'
    def eat(self):
        # Only the first super class eat function is called
        super(Dog,self).eat()
        print "Dog eating"
d = Dog()
d.eat()


# Old style class vs new style class
# 
# In the old style class, the class will not inherit from Python object class and will have access to fewer attributes and methods. 
#  
# ```
# class ClassA:
#     def method1(self):
#         pass
# ```
# 
# In new style class, the class will inherit from Python object class and will have access to more attributes and methods.
# 
# ```
# class ClassA(object):
#     def method1(self):
#         pass
# ```

# In[ ]:

'''
In-class activity: 

Create a class that takes name and age as input. If the person's age is 
greater than 18 then you should print that they are eligible to create 
a login otherwise you print that they can't create a login. Implement 
a method called compage to compare age with 18. Implement another 
method called printpermission to print the output of comparison. 
'''

