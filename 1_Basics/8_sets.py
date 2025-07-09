# Sets are unordered collections of unique elements.

# 1. Nature of Sets: mutable, unordered, unique elements
#    - No duplicates
#    - Unindexed (no slicing or direct indexing)
#    - Fast membership tests (O(1) average)

# Creating sets
set1 = {1, 2, 3, 4, 5}
print("Initial set1:", set1)

# Duplicates are removed automatically
dup_set = {1, 2, 2, 3, 4, 4, 5}
print("dup_set (duplicates removed):", dup_set)

# Empty set creation ({} creates dict)
empty = set()
print("empty set:", empty)

# 2. Adding and removing elements
set1.add(6)
print("After add(6):", set1)
set1.remove(6)  # KeyError if missing
print("After remove(6):", set1)
set1.discard(7)  # No error if missing
print("After discard(7) (no-op):", set1)

# pop(): removes and returns an arbitrary element
popped = set1.pop()
print(f"popped {popped}, remaining set1:", set1)

# clear(): remove all elements
set1.clear()
print("After clear():", set1)

# 3. Set operations
a = {1,2,3,4}
b = {3,4,5,6}
print("\na:", a, "b:", b)
print("union:", a.union(b))               # elements in either
a &= b  # intersection_update modifies a in place
print("intersection_update a &= b -> a:", a)

# Reset for examples
a = {1,2,3,4}
b = {3,4,5,6}
print("\na & b (intersection):", a.intersection(b))
print("a - b (difference):", a.difference(b))
print("b - a:", b.difference(a))
print("a ^ b (symmetric_difference):", a.symmetric_difference(b))

# 4. Subset, superset, disjoint
a = {1,2}
b = {1,2,3,4}
c = {5,6}
print("\na ⊆ b?", a.issubset(b))
print("b ⊇ a?", b.issuperset(a))
print("a is disjoint with c?", a.isdisjoint(c))

# 5. Frozenset: immutable set, can be dict key or element of another set
fs = frozenset([1,2,3])
print("\nfrozenset:", fs, type(fs))

# Note: sets are unordered, so iteration and pop() order is arbitrary.