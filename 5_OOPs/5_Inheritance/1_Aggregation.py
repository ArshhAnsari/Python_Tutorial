'''
Classes can have relationships with each other.

The two most common relationships are:

1. Aggregation (HAS-A relationship)
   One class contains or uses an object of another class.

   Examples:
   - A Customer has an Address.
   - A Restaurant has a Menu.
   - A University has Departments.

2. Inheritance (IS-A relationship)
   One class is a specialized version of another class.

   Examples:
   - A Dog is an Animal.
   - A Car is a Vehicle.
   - A Student is a Person.
'''


# =========================
# Aggregation Example
# =========================

'''
Aggregation means one class uses an object of another class.

Important:
The owning class cannot directly access private members
of the aggregated class.

For example:

Customer -> Address

If Address contains a private attribute (__pin),
Customer cannot access it directly using:

    self.address.__pin

Instead, Customer must use a public method (getter)
provided by Address.

Aggregation is often implemented by passing an object
of one class into another class.
'''


class Customer:
    def __init__(self, name, address):
        self.name = name

        # Storing a reference to an Address object.
        # Customer HAS-A Address.
        self.address = address

    def print_info(self):
        print(f"Customer Name: {self.name}")

        # Since __pin is private inside Address,
        # we access it through a getter method.
        print(f"Address Pin: {self.address.get_pin()}")

        # city and state are public attributes,
        # so they can be accessed directly.
        print(f"Address City: {self.address.city}")
        print(f"Address State: {self.address.state}")

    def edit_profile(self, new_name, new_pin, new_city, new_state):
        self.name = new_name

        # Delegating address update responsibility
        # to the Address object itself.
        self.address.edit_address(
            new_pin,
            new_city,
            new_state
        )


class Address:
    def __init__(self, pin, city, state):

        # Private attribute
        self.__pin = pin

        # Public attributes
        self.city = city
        self.state = state

    def get_pin(self):
        '''
        Getter method used to access
        the private pin value.
        '''
        return self.__pin

    def edit_address(self, new_pin, new_city, new_state):
        self.__pin = new_pin
        self.city = new_city
        self.state = new_state


# =========================
# Usage
# =========================

# Create Address object first
addr1 = Address("12345", "Anytown", "CA")

# Pass the Address object into Customer
cust = Customer("John Doe", addr1)

cust.print_info()

print()

# Modify both customer and address details
cust.edit_profile(
    "Jane Doe",
    "54321",
    "New York",
    "NY"
)

cust.print_info()


'''
=========================
Understanding the Aggregation
=========================

Step 1:
Create an Address object.

    addr1 = Address(...)

Memory:

Address Object
--------------
pin   = 12345
city  = Anytown
state = CA


Step 2:
Pass the Address object to Customer.

    cust = Customer("John Doe", addr1)

Memory:

Customer Object
---------------
name    = John Doe
address = reference to addr1


Customer does not create an Address.
It simply receives an existing Address object
and stores a reference to it.

Therefore:

    Customer HAS-A Address

This is Aggregation.


When Customer needs address information:

    self.address.get_pin()

it simply uses the Address object that was
provided to it.

Customer and Address remain separate classes.
Customer is NOT an Address.

The relationship is:

    Customer ------HAS-A------> Address
'''


# =========================
# Another HAS-A Example
# =========================

class Engine:
    def start(self):
        return "vroom"


class Car:
    def __init__(self):

        # Car creates and stores an Engine object.
        self.engine = Engine()

    def drive(self):

        # Delegating work to the Engine object.
        return self.engine.start()


car = Car()
print(car.drive())  # vroom


'''
=========================
Customer-Address vs Car-Engine
=========================

Both examples show a HAS-A relationship.

Customer -> Address
-------------------

Address object is created outside Customer.

    addr = Address(...)
    cust = Customer(..., addr)

Customer receives an already existing
Address object and uses it.

Flow:

Address created
      ↓
Passed into Customer
      ↓
Customer stores reference
      ↓
Customer uses Address methods


Car -> Engine
-------------

Engine object is created inside Car.

    self.engine = Engine()

Car itself creates and owns the Engine object.

Flow:

Car created
      ↓
Car creates Engine
      ↓
Car stores Engine
      ↓
Car uses Engine methods


Key Difference
--------------

Customer:
    Receives an Address object.

Car:
    Creates an Engine object.

Both are HAS-A relationships because one object
contains or uses another object.

Customer IS NOT an Address.
Car IS NOT an Engine.

They simply HAVE those objects and use their
functionality.


Interview Summary
-----------------

IS-A Relationship:
    Dog -> Animal
    Student -> Person

HAS-A Relationship:
    Customer -> Address
    Car -> Engine

Rule:

If object A uses or contains object B,
then A HAS-A B.

If object A is a specialized form of B,
then A IS-A B.
'''