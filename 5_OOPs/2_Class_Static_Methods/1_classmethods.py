'''Class method (@classmethod) is a method that gets the class (cls) as its first argument — use it to work with class-wide data or make alternative constructors.''' 

class Employee:
    # Class variables (shared by all instances)
    num_of_emps = 1 # Also static variable

    def __init__(self,first,last,pay):

        self.first = first # instance variable
        self.last = last
        self.pay = int(pay)
        self.email = first + '.' + last + '@company.com'
        self.cid = Employee.num_of_emps  # unique id for this instance
        Employee.num_of_emps += 1

    def full_name(self):
        return '{} {}'.format(self.first,self.last)
    
    @classmethod
    # class method is a method that is bound to the class rather than the instance
    def from_empstr(cls,emp_str):
        '''Create an Employee from a string'''
        first,last,pay = emp_str.split('-')
        return cls(first,last,int(pay))

    


emp_1 = Employee('Arsh','Ansari',50000)
emp_2 = Employee('Test','User',60000)

# Create employees using the classmethod factory from_empstr
emp_str_1 = 'John-Doe-70000'
emp_str_2 = 'Jane-Doe-80000'

new_emp_1 = Employee.from_empstr(emp_str_1)

print(emp_1.cid, emp_1.full_name(), emp_1.email)
print(new_emp_1.__dict__)
print("new_emp_1 email:", new_emp_1.email)
print("new_emp_1 pay:", new_emp_1.pay)

# class counter
print("Total employees created:", Employee.num_of_emps)

'''

Quick conceptual notes

-> Employee.num_of_emps is a class variable — shared among all Employee objects.

-> self.cid is an instance attribute — unique to each employee and created during __init__.

-> @classmethod def from_empstr(cls, ...) is a factory: it receives the class (cls), not a particular instance. cls(...) constructs and returns a new instance of the class.

-> Without the return inside from_empstr, the method would return None and new_emp_1 would not be a usable Employee object.

'''