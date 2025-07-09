# Static Method - A method that is bound to the class rather than the instance. 

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
    
    @staticmethod
    # A Method should be a static method when you dont access the instance or the class anywhere within the function
    def isweekday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return "It's weekend!"
        return "It's a work day, so Workkkk!"

    


emp_1 = Employee('Arsh','Ansari',50000)
emp_2 = Employee('Test','User',60000)

import datetime
my_date = datetime.date(2025,7,5)

print(Employee.isweekday(my_date))