'''
This Python Script is for building the logic of a Snake, Water, Gun game to run it on console

A simple Snake, Water, Gun game (variant of Rock-Paper-Scissors):
- Snake drinks Water (Snake wins)
- Water douses Gun (Water wins)
- Gun kills Snake (Gun wins)

The computer chooses randomly, and the user plays against it.
'''

import random

# Possible choices
choices = ["snake", "water", "gun"]

# Mapping of winning relationships
dwins = {
    ("snake", "water"),  # snake drinks water
    ("water", "gun"),    # water douses gun
    ("gun", "snake"),    # gun kills snake
}

print("Welcome to Snake, Water, Gun!")
print("Enter your choice: snake, water, or gun. Type 'quit' to exit.")

while True:
    user_choice = input("Your choice: ").strip().lower()
    if user_choice == "quit":
        print("Thanks for playing! Goodbye.")
        break
    if user_choice not in choices:
        print("Invalid choice. Please choose 'snake', 'water', or 'gun'.")
        continue

    comp_choice = random.choice(choices)
    print(f"Computer chose: {comp_choice}")

    if user_choice == comp_choice:
        print("It's a tie!")
    elif (user_choice, comp_choice) in dwins:
        print("You win!")
    else:
        print("You lose!")

    print()  # blank line for readability
