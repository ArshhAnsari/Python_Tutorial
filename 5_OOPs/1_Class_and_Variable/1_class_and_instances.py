class Employee:
    """
    This class represents an employee in a company.
    It has four attributes: first name, last name, pay and email.
    """

    def __init__(self,first,last,pay):
        """
        Constructor method for Employee class.
        It takes three parameters: first name, last name and pay.
        The email attribute is created by combining first name, last name and '@company.com'.
        """
        self.first = first
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

print(emp_1.__dict__)
print('\n',Employee.__dict__)