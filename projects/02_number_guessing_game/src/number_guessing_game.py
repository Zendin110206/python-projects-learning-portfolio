import random as rd

try:
    print("Welcome to the Number Guessing Game!")
    guess_count = 0
    upper_bound_text = input("Type a number to set the upper bound for the guessing game: ")
    upper_bound = int(upper_bound_text)
    secret_number = rd.randint(1, upper_bound)

    while True:
        guess_text = input("Make a guess: ")
        if not guess_text.isdigit():
            print("Please type a number next time.")
            continue
        guess = int(guess_text)
        guess_count += 1

        if guess < secret_number:
            print("You were below the number!")

        elif guess > secret_number:
            print("You were above the number!")

        else:
            print("You got it!")
            print(f"You got it in {guess_count} guesses!")
            break

except ValueError:
    print("Please type a number next time.")
