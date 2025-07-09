'''
This script illustrates key concepts of Python argument passing and sequence operations:

1. **Rebinding vs. Mutation**: How rebinding an immutable inside a function differs from mutating a mutable.
2. **Sequence Concatenation**: Using `+` to create new list or tuple objects without altering the original.
3. **In-Place Mutation**: Using list methods like `.append()` to modify the original list directly.

Each block shows the original value, the function operation, and post-call observations to clarify how Python handles object references.
'''



def reassign_number(n):
    # 'n' refers to the same integer object passed by the caller
    # n = n + 10 rebinds the local variable 'n' to a new integer object
    # This does not affect the original variable in the caller's scope
    n = n + 10
    return n        # caller's original int remains unchanged


def concat_list(lst):
    # Using '+' returns a brand-new list; original list remains unchanged
    new_list = lst + [4] # Alternative: return lst+[4]
    return new_list

def extend_list(lst):
    # Using append() mutates the original list in place
    lst.append(4)
    return lst

def concat_tuple(tup):
    # tup + (4,) creates a new tuple; original 'tup' remains unchanged
    return tup + (4,)





print("--- Rebinding | Sequence concatenation | in-place mutation examples ---")
number=10
print("\nOriginal number:",number)

# Rebinds the local variable 'number' to a new integer object
new_number = reassign_number(number)
print("\nAfter reassign_number:", new_number)
print("Original number remains:", number)

original_list = [1, 2, 3]
print("\nOriginal list:", original_list)

# concat_list returns a new list
new_lst = concat_list(original_list)
print("\nAfter concatenation:", new_lst)
print("Original list remains:", original_list)

# extend_list mutates the original list
extended = extend_list(original_list)
print("\nAfter in-place mutation(using \".append\" method):", extended)
print("Original list after in-place mutation:", original_list)

# Demonstrate tuple behavior similarly
original_tuple = (1, 2, 3)
concat_tuple = concat_tuple(original_tuple)
print("\nOriginal tuple:", original_tuple)
print("After original_tuple + (4,):", concat_tuple)
print("Original tuple remains:", original_tuple)
#    Concatenation returns a new object; append/mutation modifies in place
