class Car:
    def __init__(self, make, model, year):
        self.make = make  # Public attribute
        self.model = model  # Public attribute
        self.__odometer_reading = 0  # "Private" attribute

    # Public method
    def get_odometer_reading(self):
        """A public method to safely access the private attribute."""
        return f"This car has {self.__odometer_reading} miles on it."
    
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

# Instead, you use the public method (getter)
print(my_car.get_odometer_reading())  # Output: This car has 0 miles on it.

# Modify the state through a controlled public method
my_car.drive(150)
print(my_car.get_odometer_reading())  # Output: This car has 150 miles on it.

my_car.drive(-20) # Output: You can't drive negative miles!