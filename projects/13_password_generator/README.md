# Project 13 - Password Generator

Status: In progress.

This project is a command-line password generator. It is intended for practicing secure random selection, character sets, input validation, password length rules, and clear terminal output.

## Goal

Build a terminal program that:

- asks the user for a password length,
- validates that the length is within an allowed range,
- asks which character groups to include,
- builds an allowed character pool,
- generates a secure random password,
- guarantees that each selected character group appears at least once,
- prints the generated password clearly.

## Learning Focus

- `secrets.choice()` for secure random selection,
- `string.ascii_lowercase`, `string.ascii_uppercase`, `string.digits`, and `string.punctuation`,
- boolean input validation,
- list and string manipulation,
- password length validation,
- shuffling generated characters,
- keeping security-related code readable.

## Planned Run Command

The exact command will be finalized after the implementation is added. The intended shape is:

```powershell
python projects/13_password_generator/src/password_generator.py
```

## Expected Terminal Interaction

A valid run should look like this:

```text
Enter password length (8 - 64): 12
Include uppercase letters? (y/n): y
Include numbers? (y/n): y
Include symbols? (y/n): y
Generated password: aB7#xP2!mQ9z
```

## Completion Checklist

- The program can be run from the terminal.
- Password length input is validated.
- Yes/no options are validated.
- At least lowercase letters are always included.
- Selected character groups are included in the generated password.
- The generated password has the requested length.
- Secure randomness is used for password generation.
