# Class Methods, Static Methods, and Properties — How They Actually Function

`@classmethod`, `@staticmethod`, and `@property` look like three unrelated
decorators with three unrelated jobs. They aren't. All three are configured
versions of one single piece of machinery in Python called the **descriptor
protocol**. This note traces that machinery end to end — what happens, in
order, the instant you write `a.square(5)`, `temp.celsius`, or
`Temperature.update_highest(60)` — so that the three decorators stop being
three facts to memorize separately and become three settings on the same dial.

---

## Part 1 — The One Mechanism Underneath All Three: the Descriptor Protocol

### The idea, before any jargon

Here's the whole thing in one sentence: **in Python, a function is not just
"a thing you call" — it's also "a thing that knows how to hand itself to an
object correctly."** That second ability is called being a *descriptor*, and
it's the piece of machinery `@classmethod`, `@staticmethod`, and `@property`
all hook into. None of them invents its own system. Each one configures the
same system differently.

### What makes something a descriptor

An object is a descriptor if its **type** defines at least one of three
special methods: `__get__`, `__set__`, or `__delete__`. Nothing more
mystical than that.

Ordinary Python functions happen to implement `__get__` — easy to forget,
because you never call it yourself. You never type `my_func.__get__(...)`.
But Python does, silently, every time you write `obj.method`. That one fact
is the seed this entire note grows from.

### Two flavors, and why the split matters

```text
                    ┌─────────────────────────┐
                    │   Descriptor Protocol   │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┴───────────────────────┐
         ▼                                               ▼
┌───────────────────┐                        ┌─────────────────────┐
│  Data Descriptor  │                        │ Non-Data Descriptor │
│ (__get__  AND     │                        │   (only __get__)    │
│__set__/__delete__)│                        └──────────┬──────────┘
└────────┬──────────┘                                   │
         │                                   ┌──────────┴─────────────┐
         ▼                                   ▼                        ▼
   ┌───────────┐                     ┌────────────────┐         ┌────────────────┐
   │ @property │                     │  @classmethod  │         │  @staticmethod │
   └───────────┘                     └────────────────┘         └────────────────┘
```

A **data descriptor** defines `__get__` *and* (`__set__` or `__delete__`) —
it controls both reading and writing. A **non-data descriptor** defines only
`__get__` — it only ever intercepts reads, never writes. This split sounds
like trivia right now. It stops being trivia in Part 5, where it decides who
wins when an instance attribute and a class-level decorator share the same
name.

---

## Part 2 — The "Bouncer": How a Call Gets Its Hidden Arguments

Python does not run your function directly when you write `obj.method(...)`.
It runs it through a hidden step first — think of it as a bouncer standing at
the door, deciding what gets handed to the function before it's allowed to
execute. The bouncer's decision is entirely driven by which decorator (if any)
sits on that function. That decision is `__get__` being called.

### 1. Plain instance methods — the baseline

When you define an ordinary method and call `a.square(5)`, Python translates
that into a call to the function's `__get__`, specifically
`Function.__get__(instance, Class)`. This returns a **bound method object** —
a small wrapper that remembers `instance` and automatically inserts it as the
first argument the next time it's actually called. That inserted first
argument is `self`. You've never had to pass `self` yourself because the
bouncer is already doing it for you, on every call, without exception.

Call it on the class instead — `Class.square(instance, 5)` — and there's no
bouncer step at all: you're calling the plain function object directly, which
is why you have to pass the instance yourself in that form.

### 2. Class methods — the bouncer swaps the instance for the blueprint

`@classmethod` wraps the function in a different kind of descriptor, one whose
`__get__` behaves differently. Whether you call it as `Class.method(*args)` or
`instance.method(*args)`, this descriptor's `__get__` ignores whatever
instance you called it on and instead binds **the class itself** as the first
argument. That's `cls`. Python isn't handing the function "this particular
object" — it's handing it "the blueprint this object was stamped from."

This single behavior — "I always receive the class, never the instance" — is
exactly what makes classmethods safe to use as alternative constructors and
exactly what makes them respect subclassing: the class that gets bound is
whichever class the lookup actually resolved through, which (traced fully in
Part 6) correctly becomes the *subclass* when called through a subclass or its
instances.

### 3. Static methods — the bouncer takes the day off entirely

`@staticmethod` wraps the function in a descriptor whose `__get__` does the
least work of all three: it returns the original function completely
unchanged. No instance gets inserted. No class gets inserted. Call it as
`Class.method(*args)` or `instance.method(*args)` — either way, what actually
runs is indistinguishable from calling a plain, free-standing function that
simply happens to live inside the class's namespace for organizational
purposes.

### The three behaviors, side by side

| | What `__get__` inserts as the first argument |
|---|---|
| Plain method | the **instance** you called it on (`self`) |
| `@classmethod` | the **class** (`cls`) — regardless of whether you called it on the class or an instance |
| `@staticmethod` | **nothing** — the function runs exactly as written |

Every difference in behavior observable between these three traces back to
that one table. There is no additional rule to memorize beyond it.

---

## Part 3 — Where All of This Actually Lives: Class `__dict__` vs Instance `__dict__`

Here's a fact that trips people up precisely because the syntax looks like
you're dealing with instance attributes: **none of these three decorators
ever live in the instance's `__dict__`. All three live exclusively in the
class's `__dict__`.** What lives on the instance is only the *data* — never
the method or property object itself.

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius          # stored in the INSTANCE dict

    @property
    def area(self):
        return 3.14159 * (self.radius ** 2)

    @classmethod
    def unit_circle(cls):
        return cls(1)

    @staticmethod
    def validate_radius(r):
        return r > 0

c = Circle(5)

print(type(Circle.__dict__['area']))             # <class 'property'>
print(type(Circle.__dict__['unit_circle']))      # <class 'classmethod'>
print(type(Circle.__dict__['validate_radius']))  # <class 'staticmethod'>

print(c.__dict__)
# {'radius': 5}
# No 'area', 'unit_circle', or 'validate_radius' anywhere in here.
```

When Python executes a `class` block, it builds exactly one namespace
dictionary for that class. Each decorator's job is to take the plain function
you wrote and wrap it in its own descriptor object — a `property` object, a
`classmethod` object, a `staticmethod` object — and *that wrapper* is what
gets stored in `Circle.__dict__`, under the method's name. The instance never
receives a copy of any of this. Every instance of `Circle` shares the exact
same `area`, `unit_circle`, and `validate_radius` objects, because there's
only ever one copy, sitting on the class.

---

## Part 4 — Property as a Data Descriptor: the Gatekeeper, Mechanically

A property creates the illusion of a plain attribute while functions actually
run underneath. Here's precisely how that illusion is produced.

### Read

```python
obj.value
```

Python finds `value` in the class's `__dict__`, sees that it's a `property`
object, and calls `Property.__get__(instance, owner)`. Internally, this runs
your getter function (`fget(instance)`) and returns whatever it returns —
directly, as the value of the expression `obj.value`. There's no second step,
no parentheses needed, because `__get__` already did the calling for you.

### Write

```python
obj.value = 10
```

This is not instance-attribute assignment, even though it looks exactly like
one. Python finds `value` in the class's `__dict__`, sees it's a `property`,
and calls `Property.__set__(instance, 10)` instead of ever touching
`instance.__dict__` directly. That `__set__` call is what runs your setter
function (`fset(instance, 10)`), including whatever validation you wrote
inside it.

### The detail almost everyone misses: a property is a data descriptor *even without a setter*

This is worth sitting with, because it looks like it should be false. A
read-only property — one with only `@property` and no `@value.setter` at
all — is still classified as a **data descriptor**, not a non-data
descriptor. The reason: the `property` type itself always implements
`__set__`, regardless of whether you personally gave it a setter function. If
you never wrote a setter, that built-in `__set__` doesn't do nothing — it
actively raises `AttributeError: can't set attribute` the moment anyone tries
to assign. `property` unconditionally has both `__get__` and `__set__`
defined on its type; whether `__set__` *succeeds* or *always raises* is a
separate question from whether it *exists*. And "does it exist" is the only
thing that decides data-descriptor status. This single fact is why even a
read-only property still wins against instance-dict shadowing in Part 5 — it
doesn't need a working setter to count as a data descriptor, only the
presence of `__set__` on its type.

### Accessed through the class, not an instance

```python
Circle.area
```

Here, `instance` is `None` by the time `Property.__get__` runs — you called
it on the class itself. `property` handles this case specially: instead of
trying to run your getter on nothing, it simply hands back the raw `property`
object itself. That's exactly what makes `@value.setter` work as a decorator
in the first place — `Circle.area.setter(...)` only makes sense because
`Circle.area` returns the property object, not a computed value, when
accessed this way.

---

## Part 5 — Attribute Lookup Precedence and Shadowing

This is the payoff for having tracked data vs. non-data descriptors since
Part 1. When an instance attribute and a class-level decorator share the
exact same name, which one does `obj.name` actually resolve to? The answer
depends entirely on which *kind* of descriptor is involved, and Python's
lookup order is fixed:

```text
Data Descriptor  >  Instance __dict__  >  Non-Data Descriptor  >  Class __dict__
(highest priority)                                            (lowest priority)
```

### Scenario 1 — trying to shadow a `@property`

```python
c = Circle(5)
c.__dict__['area'] = 999          # manually poking the instance dict directly

print(c.area)                      # 78.53975 — UNCHANGED
```

`area` is a data descriptor (a `property`). Data descriptors are checked
*before* the instance `__dict__` is ever consulted, so the `999` jammed into
`c.__dict__` is simply never reached. The property's getter runs every time,
no matter what's sitting in the instance dict under that name.

### Scenario 2 — shadowing a `@classmethod` or `@staticmethod`

```python
c = Circle(5)
c.validate_radius = "I am now a string"   # assigning directly on the instance

print(c.validate_radius)            # "I am now a string"
print(Circle.validate_radius(5))    # True  — the class-level one is untouched
```

`validate_radius` is a **non-data** descriptor (`staticmethod` only
implements `__get__`). Non-data descriptors sit *below* the instance
`__dict__` in the lookup order, so the moment Python finds
`validate_radius` sitting directly on `c`, it stops looking and returns
that — the staticmethod descriptor on the class never even gets consulted
for this particular instance. The class-level version is completely
untouched; only *this one instance's* lookup was affected.

This is the entire reason the data/non-data split from Part 1 matters in
practice: it's not a classification exercise, it's what determines whether an
accidental instance-attribute collision can silently break a property (it
can't) or silently break classmethod/staticmethod access on one specific
object (it can).

---

## Part 6 — Can You Call `@classmethod` and `@staticmethod` Through an Instance?

Yes — tracing *why* it still works correctly is the real test of whether
Part 2's table actually landed.

### Calling a classmethod via an instance

```python
temp = Temperature(25)
temp.update_highest(70)
```

It's tempting to assume this should somehow pass `temp` itself into the
method, since it was called *on* `temp`. It doesn't. Lookup proceeds exactly
as always: Python walks `type(temp)`'s `__dict__` (and its MRO), finds
`update_highest` is a `classmethod` descriptor, and calls its `__get__`.
That `__get__` doesn't care what instance it was approached through — it
only cares what *class* owns the lookup, and binds that class as `cls`. The
instance `temp` is looked at just long enough to discover its type, and then
discarded entirely. `Temperature.update_highest(60)` and
`temp.update_highest(70)` produce exactly identical binding behavior; the
only difference is which object was written before the dot.

This is also precisely the mechanism that makes classmethods subclass-aware:
if `temp` were an instance of a *subclass* of `Temperature`, the lookup would
resolve `cls` to that subclass, not to `Temperature` — because `cls` is bound
to whatever class the attribute lookup actually walked through, not to
wherever the method was originally *written*.

### Calling a staticmethod via an instance

```python
temp.is_valid_celsius(-300)
```

Same lookup process, simpler outcome: Python finds `is_valid_celsius` is a
`staticmethod` descriptor and calls its `__get__`, which — as established in
Part 2 — returns the bare, unmodified function no matter what it was accessed
through. The instance isn't bound, isn't inspected for its type, isn't used
for anything at all beyond locating the method in the first place. It runs
exactly as if `Temperature.is_valid_celsius(-300)` had been written directly.

**Both forms work. Convention still prefers calling through the class name**
(`Temperature.update_highest(...)`, `Temperature.is_valid_celsius(...)`) —
not because the instance form is broken, but because reading
`Temperature.is_valid_celsius(-300)` tells another engineer, at a glance and
without opening the method body, that this call cannot possibly depend on any
particular object's state. `temp.is_valid_celsius(-300)` works identically but
reads as if it might.

---

## Part 7 — One File, Three Decorators, Full Data-Flow Trace

```python
class Temperature:
    # Class-level data — lives once, on the class, shared by every instance
    highest_recorded = 56.7

    def __init__(self, celsius):
        # This line does NOT write to instance.__dict__ directly.
        # 'celsius' is a property — this calls the SETTER.
        self.celsius = celsius

    # ── PROPERTY: the gatekeeper ──────────────────────────────
    @property
    def celsius(self):
        """Read flow: returns data out of the vault (_celsius)."""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """Write flow: validates, then stores into the vault."""
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero!")
        self._celsius = value

    # ── CLASS METHOD: always receives the blueprint ───────────
    @classmethod
    def update_highest(cls, new_temp):
        """
        __get__ binds the class as 'cls' — identically whether this
        is called via Temperature.update_highest(...) or
        some_instance.update_highest(...).
        """
        if new_temp > cls.highest_recorded:
            cls.highest_recorded = new_temp

    # ── STATIC METHOD: receives nothing extra ─────────────────
    @staticmethod
    def is_valid_celsius(value):
        """
        __get__ hands back the plain function, untouched, regardless
        of how it was accessed.
        """
        return value >= -273.15
```

### Tracing every call

```python
# ── PROPERTY ──
temp = Temperature(25)
# self.celsius = 25  ->  Property.__set__(temp, 25)
#                    ->  runs the setter, validates, sets temp._celsius = 25

print(temp.celsius)
# Property.__get__(temp, Temperature)
# -> runs the getter -> returns temp._celsius -> 25


# ── CLASS METHOD, called via the class ──
Temperature.update_highest(60)
# classmethod.__get__(None, Temperature) binds cls = Temperature
# runs as update_highest(Temperature, 60)
# 60 > 56.7  ->  Temperature.highest_recorded becomes 60

# ── CLASS METHOD, called via an instance ──
temp.update_highest(70)
# classmethod.__get__(temp, Temperature) still binds cls = Temperature
# (temp itself is never passed in) — runs as update_highest(Temperature, 70)
# 70 > 60  ->  Temperature.highest_recorded becomes 70, for EVERY instance


# ── STATIC METHOD, called via the class ──
print(Temperature.is_valid_celsius(-300))
# staticmethod.__get__(None, Temperature) returns the bare function
# runs as is_valid_celsius(-300)  ->  False

# ── STATIC METHOD, called via an instance ──
print(temp.is_valid_celsius(-300))
# staticmethod.__get__(temp, Temperature) STILL returns the bare function
# runs as is_valid_celsius(-300)  ->  False  — identical result, identical call
```

The property's two calls prove Part 4. The two `update_highest` calls prove
Part 6's classmethod case. The two `is_valid_celsius` calls prove Part 6's
staticmethod case. Every line above is a direct consequence of the single
table in Part 2 — nothing here required a new rule, only applying the same
one four different ways.

---

## Complete Comparison Matrix

| Feature | `@classmethod` | `@staticmethod` | `@property` |
|---|---|---|---|
| Descriptor classification | Non-data descriptor | Non-data descriptor | Data descriptor |
| Defines | `__get__` only | `__get__` only | `__get__` **and** `__set__` (always, even with no setter written) |
| Stored in | Class `__dict__` | Class `__dict__` | Class `__dict__` |
| First argument `__get__` inserts | the class (`cls`) | nothing | — (not a method call at all) |
| What `instance.name` evaluates to | a bound method (still needs `()`) | the plain function (still needs `()`) | the **computed result**, already evaluated — no `()` |
| Callable via `Class.name(...)` | yes | yes | n/a — accessing it via the class with no instance returns the property object itself |
| Callable via `instance.name(...)` | yes — `cls` still resolves correctly | yes — identical to the class form | n/a — reading `instance.name` already runs the getter |
| Beaten by an instance attribute of the same name? | yes (non-data descriptor loses to instance `__dict__`) | yes | **no** (data descriptor always wins) |
| Needs a setter to count as a data descriptor? | n/a | n/a | **no** — `property`'s type always has `__set__`, whether or not `.setter` was written |

---

## Self-Check — Questions, Answers, and Explanations

### Q1. `Circle.area` (a property, accessed directly on the class rather than an instance, no arguments passed) does not raise an error and does not run the getter. What does it actually return, and why does `property.__get__` special-case this instead of just running `fget` anyway?

**Answer:** It returns the `property` object itself — not a computed number,
not an error.

**Explanation:** Every getter function is written in terms of `self`
(`def area(self): return 3.14159 * (self.radius ** 2)`). Running it requires
an actual instance to supply that `self`. When `Circle.area` is accessed
instead of `c.area`, there is no instance in the picture —
`property.__get__` receives `instance=None`. Trying to run `fget(None)` would
immediately fail the moment the getter tried to read `self.radius`, since
`None` has no `radius`. Rather than let that happen, `property.__get__`
checks for exactly this case up front: if `instance is None`, it skips
calling `fget` entirely and returns the property descriptor object itself.
This isn't just an escape hatch — it's the mechanism that makes the whole
`@property` / `@x.setter` pattern work at all. `Circle.area.setter(some_func)`
only makes sense as code because `Circle.area` evaluates to the property
object (which has a `.setter` method on it), not to a number. If `__get__`
tried to run the getter unconditionally, that entire decorator chain would be
impossible to write.

---

### Q2. `instance.my_classmethod = "oops"` is assigned directly onto one specific object. Calling `instance.my_classmethod()` after that now fails (it's a string, not callable). Does `OtherInstance.my_classmethod()` on a *different* instance of the same class still work correctly? Explain using the data/non-data descriptor precedence from Part 5.

**Answer:** Yes — `OtherInstance.my_classmethod()` still works exactly as
before. The breakage is isolated to the single instance that was mutated.

**Explanation:** `classmethod` is a non-data descriptor (only `__get__`, no
`__set__`). Per the precedence order from Part 5 — Data Descriptor > Instance
`__dict__` > Non-Data Descriptor > Class `__dict__` — a non-data descriptor
sits *below* the instance `__dict__`. So for the one instance where
`my_classmethod` was directly assigned, Python's lookup finds the string
sitting right there in `instance.__dict__` and stops immediately; it never
even gets to the classmethod descriptor on the class to compare against. That
instance's `my_classmethod` attribute genuinely is just the string `"oops"`
now, which is exactly why calling it with `()` fails — strings aren't
callable.

`OtherInstance`, however, was never touched. Its own `__dict__` has no entry
named `my_classmethod`, so its lookup proceeds past the (empty) instance dict
and falls through to the class's `__dict__`, finds the `classmethod`
descriptor there, and calls its `__get__` exactly as normal — binding `cls`
and executing correctly. The shadowing in Scenario 2 of Part 5 is always
**per-instance**, never class-wide, because the thing doing the shadowing
(a plain instance-dict entry) only ever exists on the one instance it was
assigned to.

---

### Q3. A subclass `Kelvin(Temperature)` doesn't override `update_highest` at all. `Kelvin.update_highest(500)` is called. What does `cls` resolve to inside that call — `Temperature` or `Kelvin` — and which part of this note determines that?

**Answer:** `cls` resolves to `Kelvin`, not `Temperature`.

**Explanation:** When Python evaluates `Kelvin.update_highest`, it searches
`Kelvin`'s MRO (method resolution order) for an attribute named
`update_highest`. `Kelvin` itself doesn't define one, so the search continues
up to `Temperature`, where it finds the `classmethod` descriptor — this part
is ordinary attribute lookup, nothing special to classmethods yet. The
special part, covered in Part 2 and Part 6, is what happens next:
`classmethod.__get__` is called with the class the attribute was *accessed
through* — `Kelvin` — not the class where the function happens to be
*physically defined* — `Temperature`. Those are two different pieces of
information, and `classmethod.__get__` only ever uses the first one. So even
though `update_highest`'s code lives entirely inside `Temperature`, calling
it via `Kelvin` binds `cls = Kelvin` for that call. This is exactly the
"classmethods are subclass-aware" behavior named at the end of Part 2's
classmethod section, and traced in full in Part 6: `cls` always tracks
*where the lookup walked through*, never *where the method was written*.
That's also precisely why classmethods are the standard tool for alternative
constructors — `cls(*args)` inside the method correctly builds a `Kelvin`
when called as `Kelvin.from_string(...)`, without `Temperature`'s code ever
needing to know `Kelvin` exists.