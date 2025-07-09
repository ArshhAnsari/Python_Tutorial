# 1. if-elif-else statement
age=int(input("Enter your age: "))

if age <= 0:
        print("Invalid age. Age must be a positive number.")
elif age < 18:
        print("You are below the age of consent.")
else:
    # age >= 18
    if age <= 24:
            print("You are of consenting age and a fresh student.")        
    else:
            print("You are of consenting age.")


# 2. Ternary Operator
temperature=int(input("Now Enter the temperature: "))

status=(
       "Hot" if temperature > 30 else
       "Warm" if temperature > 20 else
       "Cold" if temperature > 10 else
       "Freezing" if temperature >=0 else
       "DEAD!!!"
       )
print(f"The temperature is {status}")

print("Have a nice day!")

'''
1. Traditional If-Elif-Else:
   - Used for multi-branch logic and more complex flows.
   - Evaluates conditions top-down until one is True.

2. Conditional Expression (Ternary Operator):
   Syntax:
       result = <value_if_true> if <condition> else <value_if_false>
   - Useful for quick decisions.
   - Can be nested to replace simple if-elif-else chains.

'''