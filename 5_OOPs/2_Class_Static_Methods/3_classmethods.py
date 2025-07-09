# Class Method:

class Employee:
    rasie_amt=1.04
    num_of_emps = 0

    

    def __init__(self,first,last,pay):
        
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

        Employee.num_of_emps += 1
    
    def full_name(self):
        return '{} {}'.format(self.first,self.last)
    
    @classmethod
    # class method is a method that is bound to the class rather than the instance
    def from_empstr(cls,emp_str):
        first,last,pay = emp_str.split('-')
        return cls(first,last,pay)

    


emp_1 = Employee('Arsh','Ansari',50000)
emp_2 = Employee('Test','User',60000)

emp_str_1 = 'John-Doe-70000'
emp_str_2 = 'Jane-Doe-80000'

new_emp_1 = Employee.from_empstr(emp_str_1)

print(new_emp_1.__dict__)
print(new_emp_1.email)
print(new_emp_1.pay)