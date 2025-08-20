from abc import ABC, abstractmethod

# Abstract Base Class (ABC)
# To become an abstract class, first you need to inherit from ABC class and you have to define at least one abstract method in your class
class Shape(ABC):
    @abstractmethod
    def area(self):
        """Calculate the area of the shape."""
        pass

    @abstractmethod
    def perimeter(self):
        """Calculate the perimeter of the shape."""
        pass

# Concrete subclass
class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self): # We MUST implement this method
        return self.side * self.side

    def perimeter(self): # We MUST implement this method
        return 4 * self.side

# Another concrete subclass
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

    def perimeter(self):
        return 2 * 3.14 * self.radius

# --- Usage ---

# You cannot create an instance of an abstract class
# The following line would raise a TypeError:
# my_shape = Shape()

# You can create instances of the concrete classes
my_square = Square(10)
print(f"Square Area: {my_square.area()}")       # Output: Square Area: 100
print(f"Square Perimeter: {my_square.perimeter()}") # Output: Square Perimeter: 40

my_circle = Circle(5)
print(f"Circle Area: {my_circle.area():.2f}")       # Output: Circle Area: 78.50
print(f"Circle Perimeter: {my_circle.perimeter():.2f}") # Output: Circle Perimeter: 31.40