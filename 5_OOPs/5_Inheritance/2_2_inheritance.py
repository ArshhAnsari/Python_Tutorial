# Inheritance - A way to create a new class based on an existing class


class Employee:
    # Base class for all employees
    raise_amt = 1.04
    num_of_emps = 0

    def __init__(self, first, last, pay):
        self.first = first
        self.last  = last
        self.pay   = pay
        self.email = f"{first}.{last}@company.com"

        Employee.num_of_emps += 1

    def full_name(self):
        return f"{self.first} {self.last}"

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amt)
        return self.pay


class Developer(Employee):
    # Inherits from Employee; overrides class raise_amt
    raise_amt = 1.10

    def __init__(self, first, last, pay, prog_lang):
        # Call parent constructor
        super().__init__(first, last, pay)
        self.prog_lang = prog_lang  # new attribute


class Manager(Employee):
    # Inherits from Employee; manages other Employee instances
    def __init__(self,first,last,pay,employees=None):
        super().__init__(first,last,pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self,emp):
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self,emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emps(self):
        for emp in self.employees:
            print('-->',emp.full_name())


# Create Developer instances
dev_1 = Developer('Arsh', 'Ansari', 50000, 'Python')
dev_2 = Developer('Test', 'User', 60000, 'C++')
dev_3 = Developer('Another', 'User', 70000, 'Java')

# Create Manager with initial reports
mgr_1 = Manager('Mohd_Arsh', 'Ansari', 90000, [dev_2, dev_3])
mgr_1.add_emp(dev_1)

print(f"The manager's email is: {mgr_1.email}")        # inherited attribute
print("\nThe manager's employees are:")
mgr_1.print_emps()        # list managed developers

print("\nAfter removing an employee:")
mgr_1.remove_emp(dev_2)
mgr_1.print_emps()

# Type and subclass checks
print("\nType checks:",
      isinstance(mgr_1, Manager),     # True
      isinstance(mgr_1, Employee),    # True
      isinstance(mgr_1, Developer))   # False
print("\nSubclass checks:",
  issubclass(Developer, Employee),  # True
      issubclass(Manager, Employee),    # True
      issubclass(Manager, Developer))   # False

# print(dev_1.email)
# print(dev_1.prog_lang)

# print(dev_1.pay)
# dev_1.raise_pay()
# print(dev_1.pay)


