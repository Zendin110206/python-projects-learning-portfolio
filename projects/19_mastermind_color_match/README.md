# Project 19 - Mastermind / 4 Color Match

Status: Completed.

This project is a command-line Mastermind-style color matching game. It is intended for practicing game state, random secret generation, repeated input validation, duplicate-aware scoring, and readable terminal feedback.

## Goal

Build a terminal game that:

- generates a hidden 4-color code,
- lets the player guess using valid color codes,
- allows duplicate colors in the secret code and guesses,
- validates guess length and color choices,
- scores exact position matches separately from color-only matches,
- ends when the player wins, quits, or runs out of attempts.

## Learning Focus

- generating random choices,
- validating structured terminal input,
- tracking attempts,
- comparing two sequences,
- handling duplicate colors without overcounting matches,
- separating game rules, scoring, formatting, and terminal flow.

## Run Command

From the repository root:

```powershell
python projects/19_mastermind_color_match/src/mastermind_color_match.py
```

## Expected Terminal Behavior

A valid run should show the color choices, attempt limit, and a clear prompt for each guess.

Invalid guesses should not count as attempts. The program should show exact matches and color-only matches after each valid guess, then clearly report win, quit, or game-over status.

## Completion Checklist

- The program can be run from the terminal.
- The secret code has four color codes.
- Duplicate colors are allowed.
- Guess input is normalized and validated.
- Invalid guesses do not consume attempts.
- Scoring handles duplicate colors correctly.
- Win, quit, and out-of-attempts states are clear.
- Game logic is covered by deterministic tests where practical.

## Notes

- This project uses only the Python standard library.
- Tests should use fixed secret codes instead of relying on random output.
- The duplicate-aware scoring logic is the main advanced part of this project.
- Automated tests cover parsing, validation, duplicate-aware scoring, quit, win, and out-of-attempts flows.
