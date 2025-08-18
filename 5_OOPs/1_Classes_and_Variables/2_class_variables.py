class Employee:
    # class variable which will be used to raise the salary of each employee
    rasie_amt=1.04
    # class variable which will keep track of the number of employees
    num_of_emps = 0

    def __init__(self,first,last,pay):
        # instance variables
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

        # incrementing the class variable by 1 each time a new employee is created
        Employee.num_of_emps += 1
    
    def full_name(self):
        # returning the full name of the employee
        return '{} {}'.format(self.first,self.last)
    
    def raise_pay(self):
        # raising the salary of the employee by the amount defined in the class
        self.pay = int(self.pay * self.rasie_amt)
        # [ self.pay = int(self.pay * Employee.rasie_amt) # this will also work when the raise amount is the same for all employees ]
        # returning the new salary
        # return self.pay

# creating two employees
emp_1 = Employee('Arsh','Ansari',50000)
print("Initial number of employees",Employee.num_of_emps)

emp_2 = Employee('Test','User',60000)

# printing the initial salary of the first employee
print("The pay of employee 1 is",emp_1.pay)

# changing the raise amount for the first employee
emp_1.rasie_amt =1.10
# changing the raise amount for all employees
Employee.rasie_amt =1.05

# raising the salary of both employees
emp_1.raise_pay()
emp_2.raise_pay()

# printing the salary after the raise and the raise amount for both employees
print("The pay after the arise of employee 1 is",emp_1.pay," and the raise amount is",emp_1.rasie_amt)
print("The pay of employee 2 is",emp_2.pay," and the raise amount is",emp_2.rasie_amt)

# Employee.raise_pay(emp_1) # this is when the raise amount is the same for all employees

# printing the raise amount of the class
print("The raise amount of the class is",Employee.rasie_amt)

# printing the number of employees
print("The number of employees is",Employee.num_of_emps)
