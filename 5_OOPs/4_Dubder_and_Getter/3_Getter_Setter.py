# Getter, Setter, Deleter: Properties in Python 

class Employee:
    def __init__(self,first,last):
        self.first = first
        self.last = last

    @property # Getter for email
    def email(self):
        return '{}.{}@company.com'.format(self.first,self.last)

    @property # Getter for fullname
    def fullname(self):
        return '{} {}'.format(self.first,self.last)
    
    @fullname.setter # Setter for fullname
    def fullname(self,name):
        first,last = name.split(' ')
        self.first = first
        self.last = last

    @fullname.deleter # Deleter for fullname
    def fullname(self):
        self.first = None
        self.last = None
    

emp_1 = Employee('John','Smith')
print(emp_1.fullname) # Calls fullname getter
emp_1.fullname = 'Arsh Ansari' # Calls fullname setter
emp_2 = Employee('Test','User') 
emp_2.fullname = 'Test User'
print(emp_1.first) # Calls first getter
print(emp_1.email) # Calls email getter
print(emp_1.fullname) # Calls fullname getter
del emp_2.fullname # Calls fullname deleter

print("\n",emp_1.__dict__)
print("\n",emp_2.__dict__)


