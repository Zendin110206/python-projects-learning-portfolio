# Project 03 - Rock, Paper, Scissors

Status: In progress.

This project is a beginner-friendly command-line Rock, Paper, Scissors game. The implementation is intentionally not included yet because the project is meant to be written independently as Python practice.

## Goal

Build a small terminal program that:

- asks the player to choose rock, paper, scissors, or quit,
- validates the player's input,
- randomly chooses the computer's move,
- compares both choices,
- prints whether the player won, lost, or tied,
- tracks player and computer wins,
- prints the final score when the player quits.

## Learning Focus

- importing and using `random`,
- selecting a random item from a list,
- normalizing text input,
- validating input against allowed choices,
- `while` loops,
- `continue` and `break`,
- multi-branch conditional logic,
- score counters.

## Planned Run Command

The exact command will be finalized after the implementation is added. The intended shape is:

```powershell
python projects/03_rock_paper_scissors/src/rock_paper_scissors.py
```

## Expected Terminal Interaction

Because the computer's choice is random, exact results will vary. A valid run should look like this:

```text
Type rock, paper, scissors, or q to quit: rock
Computer picked scissors.
You won!
Type rock, paper, scissors, or q to quit: q
You won 1 times.
The computer won 0 times.
Goodbye!
```

Invalid input example:

```text
Type rock, paper, scissors, or q to quit: banana
Please type rock, paper, scissors, or q.
Type rock, paper, scissors, or q to quit:
```

## Completion Checklist

- The game can be run from the terminal.
- The player can choose rock, paper, scissors, or quit.
- Input is normalized so common case variations still work.
- Invalid choices do not crash the program.
- The computer chooses randomly.
- Win, loss, and tie outcomes are handled clearly.
- Final scores are shown when the player quits.
