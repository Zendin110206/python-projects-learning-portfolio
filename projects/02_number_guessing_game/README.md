# Project 02 - Number Guessing Game

Status: Completed.

This project is a beginner-friendly command-line number guessing game. The player chooses an upper bound, the program generates a random secret number, and the player keeps guessing until the correct number is found.

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

## Run Command

From the repository root:

```powershell
python projects/02_number_guessing_game/src/number_guessing_game.py
```

## Expected Terminal Interaction

Because the secret number is random, the exact run will vary. A valid run should look like this:

```text
Welcome to the Number Guessing Game!
Type a number to set the upper bound for the guessing game: 10
Make a guess: 5
You were below the number!
Make a guess: 8
You were above the number!
Make a guess: 7
You got it!
You got it in 3 guesses!
```

Invalid upper bound example:

```text
Welcome to the Number Guessing Game!
Type a number to set the upper bound for the guessing game: zero
Please type a number next time.
```

Invalid guess example:

```text
Welcome to the Number Guessing Game!
Type a number to set the upper bound for the guessing game: 10
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

## Notes

- The secret number is random, so high/low feedback varies between runs.
- Invalid guesses do not count as attempts.
