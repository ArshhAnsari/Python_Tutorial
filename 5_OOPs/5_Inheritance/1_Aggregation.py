'''
Classes have relationships with each other.
The types in relationships include:


1. Aggregation: Has-a relationship
   Means one class is the owner of another class.
   For example, a `Customer` has an `Address`.
   `Restaurant` has a `Menu`.

2. Inheritance: Is-a relationship
   Means one class is a subclass of another class.
   For example, a `Dog` is an `Animal`.
'''

# Aggregation
'''Aggregation can not access the private members of the aggregated/owned class
so if in the `Customer` class we try to access the private members of the `Address` class, it will not be allowed.'''
# aggreation bascially ek class ke object creation me bas ek dusre class ke object ka istemal hota hai.

class Customer:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def print_info(self):
        print(f"Customer Name: {self.name}")
        print(f"Address Pin: {self.address.pin}") # if pin is a private member then it cannot be accessed, only by using a getter method or `self.address._Address__pin` but this is not recommended
        print(f"Address City: {self.address.city}")
        print(f"Address State: {self.address.state}")

    def edit_profile(self,new_name, new_pin, new_city, new_state):
        self.name = new_name
        self.address.edit_address(new_pin, new_city, new_state)


class Address:
    def __init__(self, pin, city, state):
        self.pin = pin
        # self.__pin = pin
        self.city = city
        self.state = state

    def get_pin(self):
        return self.__pin

    def edit_address(self, new_pin, new_city, new_state):
        self.pin = new_pin
        self.city = new_city
        self.state = new_state


# Usage
addr1 = Address("12345", "Anytown", "CA")
cust = Customer("John Doe", addr1)

cust.print_info()
print()
# Edit customer profile
cust.edit_profile("Jane Doe", "54321", "New York", "NY")
cust.print_info()