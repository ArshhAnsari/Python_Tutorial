"""
================================================================================
MAP, FILTER & REDUCE in Python
================================================================================

Quick Overview:
---------------
map()     → Transform every element (same length list)
filter()  → Keep only elements that pass a test (usually shorter list)
reduce()  → Combine all elements into a single value

All three accept a function as their first argument.
We will see both normal functions (def) and lambda versions.
"""

from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]
print("Original list:", numbers)
print()


# =============================================================================
# 1. map() — Transform every element
# =============================================================================
"""
Syntax:
    map(function, iterable)

What it does:
    - Takes a function and an iterable (list, tuple, etc.)
    - Applies the function to EVERY element
    - Returns a map object (we convert it to list to see the result)

Mental model:
    map( what_to_do , on_which_data )

--------------------------------------------------------------------------------
THE ACTUAL MECHANICS:
--------------------------------------------------------------------------------
map() does NOT touch the whole list at once. It is a lazy iterator that pulls
ONE element at a time from the source, feeds it to your function, and yields
the return value. Nothing computes until something consumes it (list(), a
for-loop, next()...).

For map(square, [1, 2, 3, 4, 5, 6]) the internal loop is equivalent to:

    result = []
    for x in numbers:          # pulls ONE element per iteration
        y = square(x)          # function call happens HERE, per element
        result.append(y)       # output slot filled 1-to-1 with input slot

# result has the SAME LENGTH as the input — map never drops elements

Position is preserved: input[i] → function → output[i]. That 1:1 index
mapping is the whole reason it's called "map".
"""

print("=" * 60)
print("1. map() — Transform every element")
print("=" * 60)

def square(x):
    return x * x

# ---- Manual trace: what map() is doing under the hood
print("Manual trace of map(square, numbers):")
traced_result = []
for i, x in enumerate(numbers):
    y = square(x)
    traced_result.append(y)
    print(f"  iteration {i}: input={x} → square({x})={y} | output so far: {traced_result}")
print("Final:", traced_result)
print()

squared_def = list(map(square, numbers))
print("Using def     →", squared_def)

squared_lambda = list(map(lambda x: x * x, numbers))
print("Using lambda  →", squared_lambda)

doubled = list(map(lambda x: x * 2, numbers))
print("Doubled       →", doubled)

# Convert Celsius to Fahrenheit
celsius = [0, 10, 20, 30, 40]
fahrenheit = list(map(lambda c: (9/5) * c + 32, celsius))
print("Fahrenheit    →", fahrenheit)

# map with multiple iterables
list1 = [1, 2, 3]
list2 = [10, 20, 30]
print("\nManual trace of map(lambda x, y: x+y, list1, list2):")
for i, (a, b) in enumerate(zip(list1, list2)):
    print(f"  iteration {i}: x={a}, y={b} → {a}+{b}={a+b}")
sums = list(map(lambda x, y: x + y, list1, list2))
print("Pairwise sum  →", sums)

print()
print("Note: For simple transformations, list comprehension is often cleaner:")
print("      [x * 2 for x in numbers]")
print()


# =============================================================================
# 2. filter() — Keep only elements that pass a test
# =============================================================================
"""
Syntax:
    filter(function, iterable)

What it does:
    - Takes a function that returns True or False
    - Keeps only those elements for which the function returns True
    - Removes the rest

Mental model:
    filter( condition_function , data )

--------------------------------------------------------------------------------
THE ACTUAL MECHANICS:
--------------------------------------------------------------------------------
filter() also pulls ONE element at a time, but instead of transforming it,
it runs it through a predicate (a function returning True/False) and uses
that boolean as a gate. The element itself is NEVER modified — it either
passes through unchanged or gets dropped.

Equivalent internal loop:

    result = []
    for x in numbers:
        keep = predicate(x)     # decision happens HERE, per element
        if keep:
            result.append(x)    # original value goes in untouched

# result length <= input length — filter can only shrink or keep same size

This is the key difference from map():
    map     → output length == input length  (1:1)
    filter  → output length <= input length  (some elements can vanish)
"""

print("=" * 60)
print("2. filter() — Keep elements that satisfy a condition")
print("=" * 60)

def is_even(x):
    return x % 2 == 0

print("Manual trace of filter(is_even, numbers):")
traced_evens = []
for i, x in enumerate(numbers):
    keep = is_even(x)
    if keep:
        traced_evens.append(x)
    print(f"  iteration {i}: input={x} → is_even({x})={keep} | {'KEPT' if keep else 'DROPPED'} | output so far: {traced_evens}")
print("Final:", traced_evens)
print()

evens_def = list(filter(is_even, numbers))
print("Using def     →", evens_def)

evens_lambda = list(filter(lambda x: x % 2 == 0, numbers))
print("Using lambda  →", evens_lambda)

odds = list(filter(lambda x: x % 2 != 0, numbers))
print("Odd numbers   →", odds)

students = [
    {"name": "Aman",  "marks": 91},
    {"name": "Riya",  "marks": 67},
    {"name": "Karan", "marks": 82},
    {"name": "Sneha", "marks": 55},
]

print("\nManual trace of filter(marks > 80, students):")
traced_scorers = []
for i, s in enumerate(students):
    keep = s["marks"] > 80
    if keep:
        traced_scorers.append(s["name"])
    print(f"  iteration {i}: {s['name']} marks={s['marks']} → {keep} | {'KEPT' if keep else 'DROPPED'}")

high_scorers = list(filter(lambda s: s["marks"] > 80, students))
print("High scorers  →", [s["name"] for s in high_scorers])

print()
print("Note: List comprehension is often more readable:")
print("      [x for x in numbers if x % 2 == 0]")
print()


# =============================================================================
# 3. reduce() — Collapse everything into one value
# =============================================================================
"""
Syntax:
    reduce(function, iterable)
    reduce(function, iterable, initializer)   ← optional third argument

Important:
    - You must import it → from functools import reduce
    - The function must take TWO arguments
    - It applies the function repeatedly until only one value remains

--------------------------------------------------------------------------------
THE ACTUAL MECHANICS:
--------------------------------------------------------------------------------
Unlike map/filter, reduce() carries STATE across iterations. It keeps a
running "accumulator" value. On each step it combines the accumulator
(result of ALL previous steps) with the current element, and the output
becomes the NEW accumulator for the next step.

    reduce(f, [a, b, c, d])

    step 1: acc = a           (seed — first element if no initializer given)
    step 2: acc = f(acc, b)
    step 3: acc = f(acc, c)
    step 4: acc = f(acc, d)
    return acc
"""

print("=" * 60)
print("3. reduce() — Collapse list into a single value")
print("=" * 60)

def add(x, y):
    return x + y


print("Manual trace of reduce(add, numbers):")
print("-" * 60)

"""
================================================================================
HOW reduce() WORKS INTERNALLY (Detailed Step-by-step)
================================================================================

reduce(function, iterable) follows this exact process:

1. Create an iterator from the list
2. Take the FIRST element and store it as the initial accumulator (acc)
3. Then start looping from the SECOND element onward
4. On every iteration: combine (acc + current element) and update acc
5. When the loop finishes, return the final value of acc

This is why the first number (1) never appears as 'x' in the loop —
it was already taken out as the starting accumulator.
"""

it = iter(numbers)          # Turn the list into an iterator
acc = next(it)              # Take the first element → acc = 1

print(f"  seed: acc = {acc}  (first element taken as starting value)")
print(f"  Remaining elements that will be processed: {list(it)}")
print()

# Recreate the iterator because we already consumed it above
it = iter(numbers)
acc = next(it)

for i, x in enumerate(it, start=1):
    """
    What is happening in this loop:

    - 'it' is the iterator that now starts from the SECOND element
    - 'x' receives the next remaining element on every iteration
    - 'acc' holds the result of all previous combinations

    About enumerate(it, start=1):
    -----------------------------
    enumerate() gives us both an index and the value.
    By default enumerate starts counting from 0.
    We pass start=1 so that the printed iteration numbers look natural
    to humans (Iteration 1, Iteration 2, ... instead of Iteration 0).

    It has NO effect on the actual calculation — it only affects
    the number we display in the print statement.
    """
    new_acc = add(acc, x)
    print(f"  iteration {i}: acc({acc}) + x({x}) = {new_acc}   ← acc becomes {new_acc}")
    acc = new_acc

print()
print("Final accumulator (this is what reduce returns):", acc)
print()

"""
================================================================================
DETAILED WALKTHROUGH WITH numbers = [1, 2, 3, 4, 5, 6]
================================================================================

Step 0 (before the loop):
    it = iterator over [1, 2, 3, 4, 5, 6]
    acc = next(it)  →  takes 1
    Now the iterator has remaining elements: [2, 3, 4, 5, 6]

Iteration 1:
    x = 2
    new_acc = 1 + 2 = 3
    acc becomes 3

Iteration 2:
    x = 3
    new_acc = 3 + 3 = 6
    acc becomes 6

Iteration 3:
    x = 4
    new_acc = 6 + 4 = 10
    acc becomes 10

Iteration 4:
    x = 5
    new_acc = 10 + 5 = 15
    acc becomes 15

Iteration 5:
    x = 6
    new_acc = 15 + 6 = 21
    acc becomes 21

Loop ends → reduce returns 21


================================================================================
WHY DOES THE LOOP START WITH x = 2 INSTEAD OF x = 1?
================================================================================

Because reduce() intentionally takes the first element as the starting
accumulator. It does this so that it always has a value to begin combining with.

By pulling the first element out with next(), the rest of the algorithm
becomes simple and uniform.


================================================================================
THE OPTIONAL INITIALIZER PARAMETER
================================================================================

Syntax:
    reduce(function, iterable, initializer)

If you pass a third argument (initializer), it becomes the starting
accumulator INSTEAD of taking the first element from the list.

Example:
    reduce(lambda a, b: a + b, [1, 2, 3], 10)

Internal process:
    acc = 10          ← starts from the initializer
    acc = 10 + 1 = 11
    acc = 11 + 2 = 13
    acc = 13 + 3 = 16
    returns 16

When to use initializer:
    - When you want a custom starting value
    - When the list might be empty (prevents TypeError)
    - When the type of the accumulator should be different
      from the type of the elements (e.g. starting with [] to build a list)
"""

total_def = reduce(add, numbers)
print("Using def     →", total_def)

total_lambda = reduce(lambda x, y: x + y, numbers)
print("Using lambda  →", total_lambda)

# Example with initializer
total_with_init = reduce(lambda x, y: x + y, numbers, 10)
print("With init=10  →", total_with_init)   # 21 + 10 = 31

product = reduce(lambda x, y: x * y, numbers)
print("Product       →", product)

maximum = reduce(lambda a, b: a if a > b else b, numbers)
print("Maximum       →", maximum)

# Flatten a list of lists
nested = [[1, 2], [3, 4], [5, 6]]

print("\nManual trace of reduce(flatten, nested):")
it2 = iter(nested)
acc2 = list(next(it2))   # seed = first sublist (copied so we don't mutate original)
print(f"  seed: acc = {acc2}")

for i, lst in enumerate(it2, start=1):
    new_acc2 = acc2 + lst
    print(f"  iteration {i}: acc({acc2}) + lst({lst}) = {new_acc2}")
    acc2 = new_acc2

flat = reduce(lambda acc, lst: acc + lst, nested)
print("Flattened     →", flat)

print()
print("Important Notes:")
print("  • For sum     → prefer sum(numbers)")
print("  • For product → prefer math.prod(numbers)  (Python 3.8+)")
print("  • Use reduce only when the logic is more complex")
print()


# =============================================================================
# 4. QUICK COMPARISON TABLE
# =============================================================================
print("=" * 60)
print("QUICK COMPARISON")
print("=" * 60)
print("""
| Function | Purpose                      | Per-iteration behavior                            | Returns                    |
|----------|------------------------------|---------------------------------------------------|----------------------------|
| map()    | Transform every element      | input[i] → function → output[i] (1:1, no state)   | New list (same length)     |
| filter() | Keep elements that pass test | input[i] → predicate → keep or drop (no state)    | New list (usually shorter) |
| reduce() | Combine all into one value   | acc = f(acc, input[i]) (STATE carried forward)    | Single value               |

The one-line way to tell them apart:
- map/filter build up a NEW COLLECTION as they go.
- reduce mutates ONE RUNNING VALUE, every step depends on the previous result.
""")


# =============================================================================
# 5. COMMON CONFUSION
# =============================================================================
print("=" * 60)
print("COMMON CONFUSION")
print("=" * 60)
print("""
1. map vs list comprehension
   - map(lambda x: x*2, nums)          → functional style
   - [x*2 for x in nums]               → usually more readable (preferred)

2. filter vs list comprehension
   - filter(lambda x: x > 5, nums)
   - [x for x in nums if x > 5]        → preferred in most cases

3. reduce vs built-in functions
   - Prefer sum(), max(), min(), math.prod() when they exist
   - Use reduce only for custom combining logic
""")


# =============================================================================
# 6. WHEN TO USE LAMBDA vs DEF
# =============================================================================
print("=" * 60)
print("WHEN TO USE LAMBDA vs NORMAL FUNCTION")
print("=" * 60)
print("""
Use lambda when:
  ✓ The function is very short (one expression)
  ✓ You will use it only once
  ✓ You are passing it directly to map / filter / reduce / sorted

Use def when:
  ✓ Logic is complex or needs multiple lines
  ✓ You want to reuse the function
  ✓ You want a clear name for better readability
""")


# =============================================================================
# 7. BEST PRACTICES SUMMARY
# =============================================================================
print("=" * 60)
print("BEST PRACTICES")
print("=" * 60)
print("""
1. Prefer list comprehensions for simple map and filter cases.
2. Prefer built-in functions (sum, max, min, math.prod) over reduce when possible.
3. Keep lambda expressions short and readable.
4. Always convert map() and filter() results to list() if you want to see them.
5. Remember the order:
      map(function, data)
      filter(function, data)
      reduce(function, data)
6. When debugging, mentally unroll them into the equivalent for-loop —
   that is the fastest way to see where something is going wrong.
""")

print("=" * 60)
print("END OF FILE — Map, Filter & Reduce")
print("=" * 60)