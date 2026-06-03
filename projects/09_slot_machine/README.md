# Project 09 - Slot Machine

Status: Completed.

This project is a command-line slot machine game. It is intended for practicing random weighted outcomes, input validation, balance tracking, betting rules, and small reusable functions.

## Goal

Build a terminal program that:

- asks the player to deposit an initial balance,
- lets the player choose how many lines to bet on,
- asks for a bet amount per line,
- validates the total bet against the current balance,
- generates a random slot machine spin,
- checks winning lines,
- updates the balance after each spin,
- lets the player continue playing or quit.

## Learning Focus

- numeric input validation,
- dictionaries for symbol counts and payout values,
- weighted random selection,
- nested lists for slot machine columns and rows,
- balance and total bet calculations,
- reusable functions for game steps,
- clear terminal formatting.

## Run Command

From the repository root:

```powershell
python projects/09_slot_machine/src/slot_machine.py
```

## Expected Terminal Interaction

Because slot results are random, exact symbols and winnings will vary. A valid run should look like this:

```text
What would you like to deposit? $100
Current balance is $100.
Press enter to play (q to quit).
Enter the number of lines to bet on (1-3): 2
What would you like to bet on each line? $5
You are betting $5 on 2 lines.
Total bet is $10.
A | B | D
C | C | C
B | D | A
You won $15.
You won on lines: 2
Current balance is $105.
Press enter to play (q to quit).q
You left with $105.
```

## Completion Checklist

- The program can be run from the terminal.
- Deposit input is validated.
- Bet line input is validated.
- Bet amount input is validated.
- The total bet cannot exceed the current balance.
- Slot results are generated randomly with weighted symbols.
- Winning lines are checked correctly.
- Balance changes after each spin.
- The player can quit cleanly.

## Notes

- The game uses virtual money only.
- Supported symbols are `A`, `B`, `C`, and `D`.
- The slot machine uses three rows and three columns.
- The player can bet on one to three lines per spin.
