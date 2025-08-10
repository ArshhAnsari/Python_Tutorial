class Animal:
    def speak(self):
        raise NotImplementedError("Subclass must implement this method")

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class Duck(Animal):
    def speak(self):
        return "Quack!"

# --- Usage ---
# Create a list of different animal objects
animals = [Dog(), Cat(), Duck()]

# We can iterate through them and call the same method 'speak()'
# Python doesn't care what type of animal it is, just that it has a 'speak' method.
for animal in animals:
    print(f"The animal says: {animal.speak()}")

# This function can accept any object that has a 'speak' method
def make_animal_speak(animal_object):
    print(animal_object.speak())

make_animal_speak(Dog()) # Output: Woof!
make_animal_speak(Cat()) # Output: Meow!
make_animal_speak(Duck()) # Output: Quack!