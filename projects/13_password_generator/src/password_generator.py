import secrets
import string

MIN_LENGTH = 8
MAX_LENGTH = 64


def get_password_length():
    while True:
        length_text = input(f"Enter password length ({MIN_LENGTH} - {MAX_LENGTH}): ")

        if not length_text.isdigit():
            print("Please enter a number.")
            continue

        length = int(length_text)

        if MIN_LENGTH <= length <= MAX_LENGTH:
            return length

        print(f"Password length must be between {MIN_LENGTH} and {MAX_LENGTH}.")


def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()

        if answer == "y":
            return True

        if answer == "n":
            return False

        print("Please enter y or n.")


def build_character_groups(include_uppercase, include_numbers, include_symbols):
    required_groups = [string.ascii_lowercase]

    character_pool = string.ascii_lowercase

    if include_uppercase:
        required_groups.append(string.ascii_uppercase)
        character_pool += string.ascii_uppercase

    if include_numbers:
        required_groups.append(string.digits)
        character_pool += string.digits

    if include_symbols:
        required_groups.append(string.punctuation)
        character_pool += string.punctuation

    return required_groups, character_pool


def secure_shuffle(password_chars):
    for index in range(len(password_chars) - 1, 0, -1):
        swap_index = secrets.randbelow(index + 1)
        password_chars[index], password_chars[swap_index] = (
            password_chars[swap_index],
            password_chars[index],
        )


def generate_password(length, include_uppercase, include_numbers, include_symbols):
    required_groups, character_pool = build_character_groups(
        include_uppercase, include_numbers, include_symbols
    )

    password_chars = []

    for group in required_groups:
        password_chars.append(secrets.choice(group))

    while len(password_chars) < length:
        password_chars.append(secrets.choice(character_pool))

    secure_shuffle(password_chars)

    password = "".join(password_chars)
    return password


def main():
    length = get_password_length()
    include_uppercase = ask_yes_no("Include uppercase letters? (y/n): ")
    include_numbers = ask_yes_no("Include numbers? (y/n): ")
    include_symbols = ask_yes_no("Include symbols? (y/n): ")
    password = generate_password(length, include_uppercase, include_numbers, include_symbols)
    print(f"Generated password: {password}")


if __name__ == "__main__":
    main()
