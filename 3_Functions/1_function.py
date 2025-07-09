# 1. Simple function without parameters
def avg():
    a = int(input("Enter the first number: "))
    b = int(input("Enter the second number: "))
    print(f"The average of {a} and {b} is {(a + b) / 2}")

# 2. Function with parameters and return value
def add(x, y):
    """Return the sum of x and y."""
    return x + y

# 3. Function with default arguments
def greet(name, msg="Hello"):
    """Greet someone with a custom message."""
    print(f"{msg}, {name}!")

# 4. Function with variable-length arguments
def multiply(*args):
    """Multiply any number of arguments together."""
    result = 1
    for num in args:
        result *= num
    return result

# 5. Mutable vs Immutable parameter behavior
def append_item(lst, item):
    """Appends item to list; demonstrates mutability."""
    lst.append(item)
    return lst

def reassign_number(n):
    """Attempts to reassign an immutable; original not changed."""
    n = n + 10
    return n

# Main execution
if __name__ == "__main__":
    print("--- avg() example ---")
    avg()  # uncomment to prompt user input

    print("\n--- add(3, 4) example ---")
    total = add(3, 4)
    print(f"add(3,4) = {total}")

    print("\n--- greet() examples ---")
    greet("Alice")
    greet("Bob", msg="Hi")

    print("\n--- multiply() example ---")
    product = multiply(2, 3, 4)
    print(f"multiply(2,3,4) = {product}")

    print("\n--- Mutable vs Immutable ---")
    my_list = [1, 2, 3]
    print("Before append_item:", my_list)
    append_item(my_list, 4)
    print("After append_item:", my_list)

    num = 5
    print("Before reassign_number:", num)
    new_num = reassign_number(num)
    print("After reassign_number (returned):", new_num)
    print("Original num remains:", num)



'''
Explanation of *args and argument unpacking:
-------------------------------------------
- Declaring `def func(*args):` collects all extra positional arguments into a **tuple** named `args`.
- Inside the function, `args` behaves like any tuple: you can iterate, index, unpack, etc.
- When calling a function, you can use `*` to **unpack** a sequence (tuple/list) into individual positional arguments.

Examples:
    def demo(*args):
        print(args)

    demo(1,2,3)        # args == (1,2,3)
    nums = [4,5,6]
    demo(*nums)        # same as demo(4,5,6)

This provides great flexibility when the number of arguments varies or when forwarding arguments from one function to another.
'''