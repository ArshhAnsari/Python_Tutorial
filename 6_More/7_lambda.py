"""
================================================================================
PYTHON LAMBDA FUNCTIONS
================================================================================
"""

print("SECTION 1: WHAT IS A LAMBDA FUNCTION?")
print("=" * 60)

"""
A lambda is a small *anonymous* function (a function without a name).

It is useful when you need a short, throwaway function for one-time use,
especially as an argument to another function (like sorted, map, filter).

Key characteristics:
- Anonymous (no name by default)
- Can contain only ONE expression
- Automatically returns the result of that expression
- Can take any number of arguments (including zero)
- Created with the `lambda` keyword

--------------------------------------------------------------------------------
THE ACTUAL MECHANICS:
--------------------------------------------------------------------------------
`lambda x: x * x` and `def square(x): return x * x` both create the SAME kind
of object in memory — a function object.

The only real difference is the name:
- def gives the function a name immediately
- lambda creates an anonymous function (unless you assign it to a variable)

Example:
    square_lambda = lambda x: x * x

This is actually two steps happening on one line:
1. Create an anonymous function → lambda x: x * x
2. Bind the name "square_lambda" to that function object

That's why square_lambda.__name__ shows "<lambda>" and not "square_lambda".
The function itself never received a real name.
"""

def square_normal(x):
    return x * x

square_lambda = lambda x: x * x

print("Normal function result:", square_normal(5))
print("Lambda function result:", square_lambda(5))
print()


print("SECTION 2: SYNTAX & RULES")
print("=" * 60)

"""
Official syntax:
    lambda arguments: expression

Rules:
1. Can have any number of arguments (including default values)
2. Can contain ONLY ONE expression (no multi-line code)
3. The expression is automatically returned
4. No `return` statement is allowed or needed
5. No assignments, loops, or try/except inside lambda
6. Ternary expressions (a if condition else b) ARE allowed

--------------------------------------------------------------------------------
WHY only expressions are allowed:
--------------------------------------------------------------------------------
- A statement DOES something (e.g. x = 5, for loop, print)
- An expression PRODUCES a value (e.g. x * 2, x > 5, "hello")

Lambda automatically returns the result of its expression.
That’s why you cannot write assignments or loops inside it.
"""

# Zero arguments
greet = lambda: "Hello, World!"
print("Zero args:", greet())

# One argument
double = lambda x: x * 2
print("One arg:", double(7))

# Multiple arguments
add = lambda a, b, c: a + b + c
print("Multiple args:", add(1, 2, 3))

# Default arguments
power = lambda x, n=2: x ** n
print("Default arg (square):", power(5))
print("Default arg (cube):", power(5, 3))

# Ternary expression (allowed)
is_even = lambda x: "Even" if x % 2 == 0 else "Odd"
print("Ternary:", is_even(10), is_even(7))

# These are NOT allowed (will raise SyntaxError):
# bad1 = lambda x: x = x + 1
# bad2 = lambda x: return x
# bad3 = lambda x: print(x); x + 1
print()


print("SECTION 3: LAMBDA vs REGULAR (def) FUNCTIONS")
print("=" * 60)

"""
Both create function objects, but they are used for different purposes.

| Aspect               | lambda                              | def                                |
|----------------------|-------------------------------------|------------------------------------|
| Name                 | Anonymous (<lambda>)                | Named (shows in error messages)    |
| Body                 | Only one expression                 | Any number of statements           |
| Return               | Automatic                           | You write `return`                 |
| Docstring            | Not supported                       | Fully supported                    |
| Debugging            | Harder (shows as <lambda>)          | Easier (shows function name)       |
| Best for             | Short one-time use                  | Reusable or complex logic          |

Simple rule:
- Need a name, documentation, or multiple lines? → use def
- Short one-expression function used immediately? → lambda is fine
"""

def named_func(x):
    return x * 2

anon_func = lambda x: x * 2

print("Named function __name__:", named_func.__name__)
print("Lambda function __name__:", anon_func.__name__)
print()


print("SECTION 4: BASIC EXAMPLES WITH DIFFERENT DATA TYPES")
print("=" * 60)

print("\n--- Numbers ---")
add_nums = lambda a, b: a + b
print("add_nums(10, 5) =", add_nums(10, 5))

square = lambda x: x ** 2
print("square(7) =", square(7))

print("\n--- Strings ---")
greeting = lambda name: f"Hello, {name}!"
print(greeting("Rahul"))

get_length = lambda s: len(s)
print("Length of 'Python':", get_length("Python"))

to_upper = lambda s: s.upper()
print(to_upper("hello"))

print("\n--- Lists ---")
get_first = lambda lst: lst[0]
print("First element:", get_first([10, 20, 30]))

get_last = lambda lst: lst[-1]
print("Last element:", get_last([10, 20, 30]))

print("\n--- Tuples ---")
get_second = lambda t: t[1]
print("Second item:", get_second((100, 200, 300)))

print("\n--- Dictionaries ---")
student = {"name": "Aman", "marks": 91, "age": 20}

get_marks = lambda s: s["marks"]
print("Marks:", get_marks(student))

get_name = lambda s: s.get("name", "Unknown")
print("Name:", get_name(student))
print()


print("SECTION 5: LAMBDA WITH HIGHER-ORDER FUNCTIONS")
print("=" * 60)

"""
Higher-order functions are functions that take other functions as arguments.
This is where lambda is most useful.
"""

# ---------------------------------------------------------------------------
# 5.1 sorted() and list.sort()
# ---------------------------------------------------------------------------
print("\n--- 5.1 sorted() / list.sort() ---")

"""
General structure:
    sorted(iterable, key=function, reverse=False)

- iterable  → the data you want to sort
- key       → a function that tells Python what to sort by
- reverse   → True for descending order

The key function is called once for every element.
Whatever it returns is used for comparison.

Important difference:
- sorted() returns a NEW list (original stays unchanged)
- list.sort() modifies the list in-place and returns None

--------------------------------------------------------------------------------
WHAT THE LAMBDA ACTUALLY DOES:
--------------------------------------------------------------------------------
Think of key= as a translator.

sorted() cannot directly compare dictionaries.
So it first runs every element through your lambda to convert it into
a simple value (usually a number) that it CAN compare.

Example:
    {"name": "A", "marks": 85}  →  lambda returns 85
    {"name": "B", "marks": 72}  →  lambda returns 72
    {"name": "C", "marks": 91}  →  lambda returns 91

Then sorted() just sorts these numbers and rearranges the original
dictionaries in the same order.
"""

students = [
    {"name": "A", "marks": 85},
    {"name": "B", "marks": 72},
    {"name": "C", "marks": 91},
]

print("Original students:", students)

# ---- What the lambda returns for each student, before sorting even happens
print("What key=lambda s: s['marks'] returns for each student:")
for s in students:
    print(f"  {s['name']} (marks={s['marks']}) -> lambda returns {s['marks']}")
print("sorted() then just orders these numbers: 85, 72, 91 -> 72, 85, 91 (ascending)")
print("...and rearranges the original dicts to match that order.")
print()

sorted_asc = sorted(students, key=lambda s: s["marks"])
print("\nSorted by marks ASC:", sorted_asc)

sorted_desc = sorted(students, key=lambda s: s["marks"], reverse=True)
print("Sorted by marks DESC:", sorted_desc)

"""
Mental model:
    sorted( WHAT_TO_SORT , key=HOW_TO_SORT )

- First argument = the collection
- key=lambda ... = the rule for comparison
- The name inside lambda (s, student, x, etc.) can be anything
"""

inventory = {
    "Apple": 50,
    "Banana": 30,
    "Orange": 45,
    "Mango": 20,
}

print("\nInventory:", inventory)

# When you pass a dict to sorted(), it iterates over the KEYS by default.
print("Manual trace of sorted(inventory, key=lambda k: inventory[k]):")
for i, k in enumerate(inventory):
    print(f"  call {i}: key(k='{k}') -> inventory['{k}'] = {inventory[k]}")

sorted_by_qty = sorted(inventory, key=lambda k: inventory[k])
print("Keys sorted by quantity ASC:", sorted_by_qty)

sorted_by_qty_desc = sorted(inventory, key=lambda k: inventory[k], reverse=True)
print("Keys sorted by quantity DESC:", sorted_by_qty_desc)

# Other useful examples
points = [(3, 3), (4, 2), (2, 2), (5, 2), (1, 7)]
sorted_by_product = sorted(points, key=lambda p: p[0] * p[1])
print("\nPoints sorted by x*y:", sorted_by_product)

words = ["banana", "kiwi", "strawberry", "fig", "apple"]
by_length = sorted(words, key=lambda w: len(w))
print("Words by length:", by_length)

names = ["Alan Turing", "Tim Berners-Lee", "Grace Hopper", "Linus Torvalds"]
by_last = sorted(names, key=lambda n: n.split()[-1])
print("Names by last name:", by_last)


# ---------------------------------------------------------------------------
# 5.2 max() and min()
# ---------------------------------------------------------------------------
print("\n--- 5.2 max() / min() ---")

"""
max() and min() also accept a key= function.
They use the same idea as sorted(): convert each item into a comparable value,
then find the highest or lowest one.
"""

highest = max(inventory, key=lambda k: inventory[k])
print("Product with highest quantity:", highest)

top_student = max(students, key=lambda s: s["marks"])
print("Top student:", top_student)

lowest_student = min(students, key=lambda s: s["marks"])
print("Lowest student:", lowest_student)
print()


print("SECTION 6: WORKING WITH DICTIONARIES & LISTS OF DICTS")
print("=" * 60)

"""
This is the area where beginners get most confused —
especially the difference between the first argument and the lambda parameter.
"""

print("\n--- Sorting a list of dictionaries ---")
students = [
    {"name": "A", "marks": 85, "age": 20},
    {"name": "B", "marks": 72, "age": 22},
    {"name": "C", "marks": 91, "age": 19},
]

result = sorted(students, key=lambda s: s["marks"], reverse=True)
for student in result:
    print(f"  {student['name']} → {student['marks']}")

print("\n--- Sorting dictionary keys by values ---")
inventory = {
    "Apple": 50,
    "Banana": 30,
    "Orange": 45,
    "Mango": 20,
}

sorted_keys = sorted(inventory, key=lambda k: inventory[k], reverse=True)
print("Products by quantity (desc):", sorted_keys)

sorted_items = sorted(inventory.items(), key=lambda item: item[1], reverse=True)
print("Items sorted by value:", sorted_items)

print("\n--- Why do we write 'students' or 'inventory' at the beginning? ---")
"""
Because sorted() needs to know WHAT to sort.

Mental model:
    sorted( what_to_sort , key=how_to_sort )

- First argument = the collection (list, dict, etc.)
- key=lambda ... = the rule used to decide the order

The variable inside the lambda (s, k, item, etc.) is just a temporary name
for the current element being examined. You can name it anything.
"""
print()


print("SECTION 7: ADVANCED PATTERNS & TECHNIQUES")
print("=" * 60)

# 7.1 Multiple sorting criteria
print("\n--- Multi-level sorting ---")
students_multi = [
    {"name": "Alice", "grade": "B", "score": 85},
    {"name": "Bob", "grade": "A", "score": 90},
    {"name": "Charlie", "grade": "B", "score": 92},
    {"name": "Diana", "grade": "A", "score": 88},
]

"""
When the lambda returns a TUPLE, Python compares tuples element-by-element
from left to right (just like sorting words alphabetically).

Example:
    ("A", -90) vs ("B", -85)  → "A" comes before "B" -> done, no need to check score
    ("A", -90) vs ("A", -88)  → first elements equal → compare second elements

The negative sign (-s["score"]) is a common trick to sort that field
in descending order while keeping the other field ascending.
"""

print("Manual trace of key tuples:")
for s in students_multi:
    key_tuple = (s["grade"], -s["score"])
    print(f"  {s['name']}: grade={s['grade']}, score={s['score']} → key={key_tuple}")

multi_sorted = sorted(students_multi, key=lambda s: (s["grade"], -s["score"]))
print("\nMulti-key sort result:")
for s in multi_sorted:
    print(f"  {s}")

# 7.2 Using operator module
print("\n--- Using operator.itemgetter ---")
from operator import itemgetter

# itemgetter("marks") does the same job as lambda s: s["marks"]
# but is slightly faster and cleaner in some cases.
sorted_op = sorted(students, key=itemgetter("marks"), reverse=True)
print("Using itemgetter:", sorted_op)

# 7.3 Function factory with lambda
print("\n--- Function factory with lambda ---")

"""
A factory function creates and returns new functions.

make_multiplier(2) returns a lambda that multiplies by 2.
make_multiplier(3) returns a different lambda that multiplies by 3.

Each returned lambda remembers its own value of n. 
As each call gets its own private copy of n that don't interfere with each other.
"""

def make_multiplier(n):
    return lambda x: x * n

double = make_multiplier(2) # -> double always multiplies by 2
triple = make_multiplier(3) #-> double always multiplies by 3
print("double(5) =", double(5))
print("triple(5) =", triple(5))

# 7.4 Conditional logic inside lambda
print("\n--- Conditional inside lambda ---")
classify = lambda score: "Pass" if score >= 40 else "Fail"
print(classify(75), classify(30))

grade = lambda m: (
    "A" if m >= 90 else
    "B" if m >= 80 else
    "C" if m >= 70 else
    "D" if m >= 60 else "F"
)
print("Grade for 85:", grade(85))
print()


print("SECTION 8: COMMON MISTAKES & PITFALLS")
print("=" * 60)

print("\n--- Mistake 1: Late-binding closure in loops ---")

"""
This is the #1 most common bug with lambdas.
"""

# THE BUGGY VERSION
multipliers = [lambda x: x * i for i in range(3)]
print("Buggy results:", [f(10) for f in multipliers])   # [20, 20, 20]

"""
================================================================================
WHY ALL LAMBDAS REMEMBER THE FINAL VALUE (i = 2)
================================================================================

In Python, the loop variable `i` is ONE shared variable.
On every iteration, its value is simply overwritten.

When you write:

    multipliers = [lambda x: x * i for i in range(3)]

Python does this behind the scenes:

    1. Create an empty list
    2. Start a loop: for i in range(3)
    3. On every iteration, create a NEW lambda function object
    4. Put that lambda object into the list
    5. After the loop finishes, the list contains 3 lambda objects

So the timeline looks like this:

    Start of loop
    -------------------------------------------------
    iteration 0:
        i = 0
        create lambda #0
        this lambda does NOT store the number 0
        it stores a REFERENCE to the variable named "i"

    iteration 1:
        i = 1          ← same variable is overwritten
        create lambda #1
        this lambda also stores a REFERENCE to the same variable "i"

    iteration 2:
        i = 2          ← same variable is overwritten again
        create lambda #2
        this lambda also stores a REFERENCE to the same variable "i"

    Loop ends.
    At this moment, the variable `i` permanently holds the value 2.

Now when we later call the lambdas:

    multipliers[0](10)   → looks up current value of i → finds 2 → 10 * 2 = 20
    multipliers[1](10)   → looks up current value of i → finds 2 → 10 * 2 = 20
    multipliers[2](10)   → looks up current value of i → finds 2 → 10 * 2 = 20

All three lambdas are looking at the SAME variable `i`,
and by the time they are called, that variable has already finished at 2.

This behavior is called "late binding":
    The name `i` is looked up at CALL time, not at CREATION time.


================================================================================
THE FIX — DEFAULT ARGUMENT TRICK (i=i)
================================================================================
"""

# THE FIXED VERSION
multipliers_fixed = [lambda x, i=i: x * i for i in range(3)]
print("Fixed results:", [f(10) for f in multipliers_fixed])  # [0, 10, 20]

"""
Why `i=i` works:

Default argument values are evaluated at the moment the function is CREATED,
not when it is called.

So each lambda receives its own private copy of the current value of i:

    So the timeline now becomes:

    iteration 0:
        current value of i is 0
        create lambda with default argument i=0
        → this lambda now has its OWN private copy of the number 0

    iteration 1:
        current value of i is 1
        create lambda with default argument i=1
        → this lambda has its OWN private copy of the number 1

    iteration 2:
        current value of i is 2
        create lambda with default argument i=2
        → this lambda has its OWN private copy of the number 2

Now each lambda has its own independent value.

When we call them later:

    multipliers_fixed[0](10)  → uses its private i=0  → 10 * 0 = 0
    multipliers_fixed[1](10)  → uses its private i=1  → 10 * 1 = 10
    multipliers_fixed[2](10)  → uses its private i=2  → 10 * 2 = 20

================================================================================
[] vs () difference
================================================================================

[ expression for ... ]  → List comprehension
    - Runs immediately
    - Creates all lambdas right away

( expression for ... )  → Generator expression
    - Does not run immediately
    - Returns a generator object
    - Creates lambdas only when you iterate over it

================================================================================
MENTAL MODEL
================================================================================

1. List comprehension runs the loop immediately.
2. The loop variable is shared and gets overwritten.
3. A normal lambda closes over the variable by REFERENCE (late binding).
4. Therefore every lambda sees whatever value the variable has at CALL time.
5. Using i=i takes a snapshot of the value at CREATION time.
"""

print("\n--- Mistake 2: Assigning lambda to a name ---")
"""
PEP 8 recommends against this style:

    square = lambda x: x * x     # discouraged

Prefer:

    def square(x):
        return x * x

Named functions give better error messages and are clearer.
"""

print("\n--- Mistake 3: Putting statements inside lambda ---")
"""
These are illegal:
    lambda x: x = x + 1
    lambda x: return x * 2
    lambda x: print(x)
"""

print("\n--- Mistake 4: Overly complex lambdas ---")
"""
If the expression becomes hard to read, convert it to a normal function.
Readability is more important than cleverness.
"""

print("\n--- Mistake 5: Using lambda when a built-in already exists ---")
"""
Bad:   sorted(nums, key=lambda x: abs(x))
Good:  sorted(nums, key=abs)

Bad:   reduce(lambda a, b: a + b, nums)
Good:  sum(nums)
"""
print()


print("SECTION 9: BEST PRACTICES & WHEN NOT TO USE LAMBDA")
print("=" * 60)

"""
WHEN TO USE LAMBDA:
- As the key= argument to sorted(), max(), min()
- Short one-off functions for map(), filter(), reduce()
- Simple callbacks
- When the function is used only once and has no good name

WHEN NOT TO USE LAMBDA:
- When the logic needs more than one expression
- When you need a docstring or type hints
- When the function will be reused
- When readability suffers
- When a built-in function already does the job
- When you feel the urge to assign it to a variable → use def instead

PEP 8 guidance:
"Always use a def statement instead of an assignment statement that binds
a lambda expression directly to an identifier."
"""
print()


print("SECTION 10: COMPLETE REAL-WORLD EXAMPLES")
print("=" * 60)

print("\n--- Example 1: E-commerce product sorting ---")
products = [
    {"name": "Laptop", "price": 75000, "rating": 4.5, "stock": 12},
    {"name": "Mouse", "price": 800, "rating": 4.2, "stock": 50},
    {"name": "Keyboard", "price": 2500, "rating": 4.7, "stock": 30},
    {"name": "Monitor", "price": 18000, "rating": 4.4, "stock": 8},
]

sorted_products = sorted(
    products,
    key=lambda p: (-p["rating"], p["price"])
)
print("Best rated, then cheapest:")
for p in sorted_products:
    print(f"  {p['name']}: ₹{p['price']} (★{p['rating']})")

print("\n--- Example 2: Filtering + sorting students ---")
all_students = [
    {"name": "Aman", "marks": 91, "city": "Delhi"},
    {"name": "Riya", "marks": 67, "city": "Mumbai"},
    {"name": "Karan", "marks": 82, "city": "Delhi"},
    {"name": "Sneha", "marks": 55, "city": "Pune"},
    {"name": "Vikram", "marks": 78, "city": "Mumbai"},
]

"""
Note the ORDER of operations here — filter runs first (lazily), and sorted()
is what actually forces iteration through the filter object. filter() itself
produces nothing until something (sorted, in this case) pulls from it.
"""
delhi_toppers = sorted(
    filter(lambda s: s["city"] == "Delhi" and s["marks"] > 70, all_students),
    key=lambda s: s["marks"],
    reverse=True
)
print("Delhi students with marks > 70:")
for s in delhi_toppers:
    print(f"  {s['name']}: {s['marks']}")

print("\n--- Example 3: Grade conversion pipeline ---")
raw_scores = [45, 78, 92, 33, 61, 88, 55]

grades = list(map(
    lambda m: "A" if m >= 90 else "B" if m >= 75 else "C" if m >= 60 else "D" if m >= 40 else "F",
    raw_scores
))
print("All grades:", grades)

good_grades = list(filter(lambda g: g in ("A", "B"), grades))
print("Good grades only:", good_grades)
print()


print("=" * 60)
print("SECTION 11: QUICK REFERENCE SUMMARY")
print("=" * 60)

print("""
SYNTAX
    lambda arguments: expression

MOST COMMON PATTERNS
    # Sort list of dicts by a key
    sorted(data, key=lambda item: item["key_name"], reverse=True)

    # Sort dict keys by their values
    sorted(my_dict, key=lambda k: my_dict[k])

    # Max / Min with custom key
    max(data, key=lambda item: item["key_name"])

    # Transform
    list(map(lambda x: x * 2, numbers))

    # Filter
    list(filter(lambda x: x > 10, numbers))

DATA TYPE CHEAT SHEET
    Number        → lambda x: x * 2
    String        → lambda s: s.upper()
    List          → lambda lst: lst[0]
    Tuple         → lambda t: t[1]
    Dictionary    → lambda d: d["marks"]
    Dict in list  → lambda s: s["marks"]

MENTAL MODELS
1. lambda just creates an anonymous function object, nothing special
happens until something CALLS it.
2. sorted/max/min with key= call your lambda ONCE per element (decorate),
then compare only the returned values, never your original data.
3. A lambda closes over surrounding VARIABLES by reference, not by
value snapshot — this is why loop variables leak into lambdas
unless you force a copy with a default argument (i=i).
4. Tuple keys compare left to right, stopping at the first field that
isn't tied — that's how multi-level sorts work with a single key=.

GOLDEN RULES
1. Keep lambdas short and readable.
2. Prefer list comprehensions over map/filter + lambda for simple cases.
3. Prefer def when the function needs a name or complex logic.
4. First argument of sorted/max/min = WHAT to process
   key=lambda ... = HOW to process each element
5. The variable name inside lambda is temporary — choose any clear name.
""")

print("=" * 60)