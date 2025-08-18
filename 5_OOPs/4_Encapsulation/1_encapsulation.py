# Encapsulation in Python
# Encapsulation is a fundamental concept in object-oriented programming that helps to keep an object's internal state safe from outside interference and misuse. It achieves this by hiding the object's attributes and providing controlled access to them through public methods.

# In Python, encapsulation is achieved by using functions (or methods) to manipulate the object's internal state. This way, the internal state of the object is protected from direct access by external code. Instead, other code relies on the provided public methods to interact with the object.

# By encapsulating the object's internal state, we can ensure that the object behaves correctly and maintains its integrity. This is important because it helps to prevent bugs and makes the code easier to understand and maintain.

# In the `Car` class example, we have created private attributes (`__odometer_reading`) that are not directly accessible from outside the class. Instead, we provide public methods (`get_odometer_reading` and `drive`) to manipulate the private attribute in a controlled way.

# This encapsulation helps to ensure that the `Car` object's internal state is kept safe and that it behaves correctly. It also makes it easier for other developers to work with the `Car` class, as they need to rely on the provided public methods to interact with the object.

class Car:
    def __init__(self, make, model, year):
        self.make = make  # Public attribute
        self.model = model  # Public attribute
        self.__odometer_reading = 0  # "Private" attribute

    # Getter for odometer reading
    def get_odometer_reading(self):
        """A public method to safely access the private attribute."""
        return f"This car has {self.__odometer_reading} miles on it."

    # Setter for odometer reading
    def drive(self, miles):
        """A public method to modify the private attribute in a controlled way."""
        if miles >= 0:
            self.__odometer_reading += miles
        else:
            print("You can't drive negative miles!")

# --- Usage ---
my_car = Car("Toyota", "Camry", 2023)

# You can access public attributes directly
print(f"My car is a {my_car.make} {my_car.model}.")

# You can't directly access the "private" attribute easily
# The following line would cause an AttributeError:
# print(my_car.__odometer_reading)
# print (my_car._Car__odometer_reading)  # This works because now the private attribute is named in the memory as _Car__odometer_reading, but it's not recommended 
# Instead, you use the public method (getter)
print(my_car.get_odometer_reading())  # Output: This car has 0 miles on it.

# Modify the state through a controlled public method
my_car.drive(150)
print(my_car.get_odometer_reading())  # Output: This car has 150 miles on it.

my_car.drive(-20) # Output: You can't drive negative miles!