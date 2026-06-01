# Project 01 - Quiz Game

Status: In progress.

This project is a beginner-friendly command-line quiz game. The implementation is intentionally not included yet because the project is meant to be written independently as Python practice.

## Goal

Build a small terminal program that:

- welcomes the player,
- asks whether they want to play,
- asks a short set of questions,
- checks each answer,
- tracks the score,
- prints the final score and percentage.

## Learning Focus

- `print()`
- `input()`
- strings and casing
- conditional logic
- variables
- simple arithmetic
- command-line execution

## Planned Run Command

The exact command will be finalized after the implementation is added. The intended shape is:

```powershell
python projects/01_quiz_game/src/quiz_game.py
```

## Expected Terminal Interaction

Example all-correct run:

```text
Welcome to the Computer Quiz!
Do you want to play? yes
Okay, let's play!

What does CPU stand for? central processing unit
Correct!

What does GPU stand for? graphics processing unit
Correct!

What does RAM stand for? random access memory
Correct!

What does PSU stand for? power supply
Correct!

You got 4 questions correct.
You got 100.0%.
```

Example early exit:

```text
Welcome to the Computer Quiz!
Do you want to play? no
Maybe next time.
```

## Completion Checklist

- The game can be run from the terminal.
- The player can choose whether to play.
- Answers are checked without being sensitive to uppercase/lowercase input.
- The final score is shown clearly.
- The final percentage is calculated correctly.
- The README is updated when the implementation is complete.
