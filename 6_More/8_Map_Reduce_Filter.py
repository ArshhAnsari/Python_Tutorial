from functools import reduce

lst = [1,2,3,4,5]

print("The original list is: ",lst)

print("# Map Example: ",end="")
def square(x):
    return x*x

print(list(map(square, lst)))

print("# Filter Example: ",end="")
def is_even(x):
    return x % 2 == 0

print(list(filter(is_even, lst)))

print("# Reduce Example: ",end="")
# reduce(function, sequence) works in sequence
def sum(x,y):
    return x+y
print(reduce(sum,lst))