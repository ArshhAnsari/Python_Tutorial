'''
Inheritance lets a class (child/subclass) reuse and extend the behavior of another class (parent/base class). 
The child automatically has the methods and attributes of the parent unless the child overrides them.
This enables code reuse and lets you model “is-a” relationships: A Student is a User.

WWhat gets inherited?
    Constructor
    Non-Private Attributes
    Non-Private Methods
'''

# Example:

# Parent-Class
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def login(self):
       print('login successful')

# Child-Class  
class Student(User):
    def __init__(self):
        self.student_id = 100

    def study(self):
        print("Is studying.")

# Create instances
u=User('Alice', 30)
s=Student()

s.login() # Prints login successful
s.study() # Prints Is studying.
print(s.name) # Why AttributeError: 'Student' object has no attribute 'name' ?

'''

## Why it causes the `AttributeError` 

1. You instantiate `s = Student()`.
    Python creates a new `Student` object (calls `__new__` under the hood), then calls `Student.__init__` to initialize it.

2. `Student.__init__` runs, and its body is:

   ```python
   def __init__(self):
       self.student_id = 100
   ```

   * This sets only `student_id` on the new object.
   * It does NOT set `name` or `age`, because `Student.__init__` does not call `User.__init__`.

3. Later you do `print(s.name)` or `s.study()` which tries to use `self.name`.

   * Python looks for `name` on the instance and then on the class chain; it is **not found** because `User.__init__`, which would have created `self.name`, was never executed.
   * Result: `AttributeError: 'Student' object has no attribute 'name'`.

** Important point: When a subclass defines its own `__init__`, Python **does not** implicitly call the parent class’s `__init__`.
                    You must call the parent `__init__` explicitly if you want its initialization behavior.

------------------------------------------------------------------------------------------------------------

## How attribute lookup & inheritance run (concise mechanics)

* During `s = Student()`:

  * `Student.__new__` (inherits `object.__new__` unless overridden) allocates the object.
  * Python calls `Student.__init__(s, ...)` with whatever args you supplied.
  * If `Student.__init__` does not call `User.__init__`, the parent initialization never happens.

* When you access `s.name`:

  * Python checks `s.__dict__` for `'name'`.
  * If not found, it checks `Student.__dict__`, then `User.__dict__`, then bases following the MRO.
  * Because `name` was supposed to be set by `User.__init__` on the instance, and that never ran, it’s missing.

When you define `__init__` in `Student`, you override `User.__init__`. Python runs the child’s `__init__` instead of the parent’s, so any initialization that `User.__init__` would have done (like setting `self.name`) doesn’t happen — unless you explicitly call it. 
`super()` is the clean, recommended way to call the parent’s `__init__` so the parent’s initialization runs too.

super().__init__(...) says: “Run the next __init__ in the method-resolution order (usually the parent) so it can set up its part of the object.”
Without super(), the parent’s setup is skipped and attributes it creates won’t exist on the instance — hence AttributeError.

> Correct usage with super():

# Parent
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def login(self):
        print('login successful')

# Child fixed to call parent initializer
class Student(User):
    def __init__(self, name, age, student_id=100):
        # call User.__init__ to set name and age on the instance
        super().__init__(name, age)
        # then set Student-specific attributes
        self.student_id = student_id

    def study(self):
        print(f"{self.name} is studying.")


u = User('Alice', 30)
s = Student('Bob', 20)   # now pass name and age to Student

print(s.name)   # works: 'Bob'
s.login()       # works: login successful
s.study()       # works: 'Bob is studying.'

Extra notes you’ll want to remember

    Match signatures: If User.__init__ requires arguments, Student.__init__ must accept them (and pass them to super()).

    When to omit super(): If the subclass intentionally doesn’t need the parent’s initialization (rare), you can skip calling it — but then you must set all needed attributes yourself.

    Why prefer super(): It cooperates with multiple inheritance and MRO; direct calls like User.__init__(self, ...) don’t.

    Not just __init__: Same idea applies to overriding any method — if you want the parent behavior plus extra behavior, call super().method(...) inside your override.

Tiny checklist

    Did you override __init__? → If yes, decide whether to call super().__init__(...).

    Do you need parent attributes or behavior? → Then call super() with correct args.

    Using multiple inheritance? → Definitely prefer super() (cooperative MRO).

Summary:
    > A class can inherit from another class.
    > Inheritance improves code reuse.
    > Constructor, attributes, and methods get inherited to the child class.
    > The parent has no access to the child class.
    > Private has no access to the child class.
    > Child class can override the attributes or methods. This is called method overriding.
    > Super() is an inbuilt function which is used to include the parent class methods and constructor.
'''