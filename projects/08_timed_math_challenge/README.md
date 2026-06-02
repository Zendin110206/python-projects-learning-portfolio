# Project 08 - Timed Math Challenge

Status: Completed.

This project is a command-line timed arithmetic challenge. It is intended for practicing random problem generation, timing with Python, loops, validation, and basic performance feedback.

## Goal

Build a terminal program that:

- waits for the player to start,
- generates a fixed number of arithmetic problems,
- asks the player to solve each problem,
- counts incorrect attempts,
- measures how long the challenge takes,
- prints the final time and mistake count.

## Learning Focus

- `random.randint()` for operands,
- `random.choice()` for operators,
- safe arithmetic evaluation,
- `time.time()` for elapsed time,
- nested loops for retrying a problem,
- input validation,
- formatted terminal output.

## Run Command

From the repository root:

```powershell
python projects/08_timed_math_challenge/src/timed_math_challenge.py
```

## Expected Terminal Interaction

Because problems are random, exact numbers will vary. A valid run should look like this:

```text
Press enter to start.
----------------------
Problem #1: 8 + 4 = 12
Problem #2: 9 * 3 = 27
...
----------------------
Nice work! You finished in 18.42 seconds.
You made 0 incorrect attempts.
```

## Completion Checklist

- The program can be run from the terminal.
- Problems are generated randomly.
- Addition, subtraction, and multiplication are supported.
- Incorrect answers are counted.
- The player retries a problem until the answer is correct.
- Total elapsed time is printed clearly.

## Notes

- The challenge uses 10 randomly generated problems.
- Supported operators are addition, subtraction, and multiplication.
- Incorrect text input is treated as a wrong answer and the same problem is retried.
