'''Static method (@staticmethod) is a plain function placed inside a class — it does not get self or cls
and is used for utility functions logically related to the class.'''

class Employee:
    raise_amt=1.04
    __num_of_emps = 0 # (private) counter # double-underscore -> name-mangled to _Employee__num_of_emps

    

    def __init__(self,first,last,pay):
        
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

        Employee.__num_of_emps += 1

    def full_name(self):
        return '{} {}'.format(self.first,self.last)
    
    @staticmethod
    def print_num_of_emps():
        '''
        Print the current count of Employee instances.
        Note: Accesses the private class variable directly from the class (Employee.__num_of_emps).
        Static method is used here because we don't need `self` or `cls`.
        '''
        print("Number of Employees:", Employee.__num_of_emps)

    @staticmethod
    def isweekday(day):
        """
        Return True if `day` is a weekday (Mon-Fri), False for weekend (Sat-Sun).

        Example:
            >>> Employee.is_weekday(datetime.date(2025, 7, 5))
            False
        """
        if day.weekday() == 5 or day.weekday() == 6:
            return "It's weekend!"
        return "It's a work day, so Workkkk!"

    


emp_1 = Employee('Arsh','Ansari',50000)
emp_2 = Employee('Test','User',60000)
print(emp_1.full_name(), emp_1.email)
emp_2.print_num_of_emps()
print(Employee._Employee__num_of_emps)  # Call static method to print employee count

import datetime
my_date = datetime.date(2025, 7, 5)

if Employee.isweekday(my_date):
    print(f"{my_date} is a work day.")
else:
    print(f"{my_date} is a weekend day.")

# Quick conceptual notes:

# -> Employee.__num_of_emps is a private (name-mangled) class variable; it is incremented when each Employee is created.
# -> @staticmethod def print_num_of_emps() prints the private counter; it doesn't receive self or cls.
# -> @staticmethod def is_weekday(day) returns a boolean telling whether the provided date is a weekday.
# -> Static methods are ideal when you need a function inside the class namespace but don't need access
#    to instance or class state (i.e., no self / cls).