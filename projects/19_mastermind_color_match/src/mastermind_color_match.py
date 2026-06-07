import random as rd
from collections import Counter

CODE_LENGTH = 4
MAX_ATTEMPTS = 10
VALID_COLORS = ("R", "G", "B", "Y", "W", "P")

COLOR_NAMES = {"R": "Red", "G": "Green", "B": "Blue", "Y": "Yellow", "W": "White", "P": "Purple"}


def generate_secret_code():
    secret_code = rd.choices(VALID_COLORS, k=CODE_LENGTH)
    return secret_code


def format_secret_code(secret_code):
    return " ".join(secret_code)


def format_valid_colors():
    formatted_colors = []
    for color in VALID_COLORS:
        formatted_colors.append(f"{color}={COLOR_NAMES[color]}")

    return ", ".join(formatted_colors)


def parse_guess(guess_text):
    if guess_text.strip().upper() == "Q":
        return "quit"

    guess = guess_text.strip().upper().split()
    return guess


def validate_guess(guess):
    if len(guess) != CODE_LENGTH:
        return "invalid_length"

    if any(color not in VALID_COLORS for color in guess):
        return "invalid_color"

    return "valid"


def score_guess(secret_code, guess):
    # return (exact_matches, color_only_matches)
    exact_matches = 0
    color_only_matches = 0

    remaining_secret_colors = []
    remaining_guess_colors = []

    for index, color in enumerate(guess):
        if color == secret_code[index]:
            exact_matches += 1
        else:
            remaining_secret_colors.append(secret_code[index])
            remaining_guess_colors.append(color)

    secret_counter = Counter(remaining_secret_colors)
    guess_counter = Counter(remaining_guess_colors)

    color_only_matches = sum((secret_counter & guess_counter).values())

    return exact_matches, color_only_matches


def print_intro():
    print("Mastermind - 4 Color Match")
    print(f"Valid colors: {format_valid_colors()}")
    print("Guess the 4-color secret code. Duplicates are allowed.")
    print(f"You have {MAX_ATTEMPTS} attempts.")


def play_game():
    secret_code = generate_secret_code()
    print_intro()

    attempt_number = 1

    while attempt_number <= MAX_ATTEMPTS:
        guess_text = input(f"Enter guess #{attempt_number}: ")

        guess = parse_guess(guess_text)

        if guess == "quit":
            print(f"Game ended. Secret code was: {format_secret_code(secret_code)}")
            return

        validation_status = validate_guess(guess)

        if validation_status == "invalid_length":
            print("Enter exactly 4 colors.")
            continue

        elif validation_status == "invalid_color":
            print(f"Use only valid color codes: {', '.join(VALID_COLORS)}.")
            continue

        exact_matches, color_only_matches = score_guess(secret_code, guess)

        print(f"Exact matches: {exact_matches}")
        print(f"Color-only matches: {color_only_matches}")

        if exact_matches == CODE_LENGTH:
            print(f"You cracked the code in {attempt_number} attempts.")
            return

        attempt_number += 1

    print(f"Out of attempts. Secret code was: {format_secret_code(secret_code)}")


if __name__ == "__main__":
    play_game()
