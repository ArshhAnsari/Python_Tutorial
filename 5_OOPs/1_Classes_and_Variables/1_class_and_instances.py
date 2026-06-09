"""
A class is an object that knows how to produce other objects.
Not just a template sitting idle. In Python, the class itself is a live object in memory, with its own type, identity, and attributes. 
When you call Dog("Bruno"), the class actively participates in creating the instance.

class Dog:
    pass

print(type(Dog))    # <class 'type'>  ← the class IS an object, of type 'type'
print(id(Dog))      # memory address — it exists right now

What Actually Happens When Call Dog("Bruno"):

Dog("Bruno")
    │
    ├─ Step 1: __new__(Dog)   → creates a blank instance in memory
    │                           returns the empty object
    │
    └─ Step 2: __init__(instance, "Bruno")  → initializes it
                                              sets attributes on the object
                                              returns None

__init__ — What It Is and Is Not
__init__ is not a constructor. It does not create the object. 
The object already exists by the time __init__ runs. __init__ is an initializer — it sets up the freshly created object.
"""
class Employee:
    """
    This class represents an employee in a company.
    It has four attributes: first name, last name, pay and email.
    """

    def __init__(self,first,last,pay): #
        """
        Constructor method for Employee class.
        It takes three parameters: first name, last name and pay.
        The email attribute is created by combining first name, last name and '@company.com'.
        """
        self.first = first # 'self' here is the blank instance just created # self.first = first means: attach attribute 'first' to that instance
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'
    
    def full_name(self):
        """
        This method returns the full name of the employee.
        It uses the format method to combine first name and last name with a space in between.
        """
        # return self.first + " " +self.last
        # return f"{self.first} {self.last}"
        return '{} {}'.format(self.first,self.last)
   

emp_1 = Employee('Arsh','Ansari',50000)
emp_2 = Employee('Test','User',60000)

print(emp_1.email)
# Using the instance to call the method
print(emp_1.full_name())  # This calls the full_name method on the emp_1 instance.

# Using the class to call the method by passing the instance
print(Employee.full_name(emp_1))  # This calls the full_name method of the Employee class, passing emp_1 as the argument.

"""
When you call emp_1.full_name(), Python translates it to this:

emp_1.full_name() -> is exactly equivalent to -> Employee.full_name(emp_1)
Python takes the instance emp_1 and passes it as the first argument to the function. 
That first parameter is what you name self. You could name it anything — self is just what everyone uses.

Both lines produce the same output. emp_1.full_name() is syntactic sugar.
"""


print(emp_1.__dict__)
print('\n',Employee.__dict__)