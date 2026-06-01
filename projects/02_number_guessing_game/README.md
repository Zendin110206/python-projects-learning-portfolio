# Project 02 - Number Guessing Game

Status: In progress.

This project is a beginner-friendly command-line number guessing game. The implementation is intentionally not included yet because the project is meant to be written independently as Python practice.

## Goal

Build a small terminal program that:

- asks the player for the upper bound of the guessing range,
- validates that the upper bound is a positive number,
- generates a random secret number inside the range,
- repeatedly asks the player to make a guess,
- validates that each guess is numeric,
- tells the player whether each guess is too high or too low,
- stops when the player guesses correctly,
- prints how many guesses were needed.

## Learning Focus

- importing and using `random`,
- numeric input validation,
- converting strings to integers,
- `while` loops,
- `continue` and `break`,
- comparison logic,
- counting attempts.

## Planned Run Command

The exact command will be finalized after the implementation is added. The intended shape is:

```powershell
python projects/02_number_guessing_game/src/number_guessing_game.py
```

## Expected Terminal Interaction

Because the secret number is random, the exact run will vary. A valid run should look like this:

```text
Type a number: 10
Make a guess: 5
You were below the number!
Make a guess: 8
You were above the number!
Make a guess: 7
You got it!
You got it in 3 guesses.
```

Invalid upper bound example:

```text
Type a number: zero
Please type a number next time.
```

Invalid guess example:

```text
Type a number: 10
Make a guess: abc
Please type a number next time.
Make a guess:
```

## Completion Checklist

- The game can be run from the terminal.
- The upper bound must be a positive number.
- The secret number is generated randomly inside the chosen range.
- Invalid guesses do not crash the program.
- The player receives high/low feedback.
- The game stops after the correct guess.
- The final attempt count is shown clearly.
