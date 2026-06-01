# Project 06 - PIG Dice Game

Status: In progress.

This project is a command-line implementation of the PIG dice game. It is intended for practicing loops, turn-based game state, score tracking, and random dice rolls.

## Goal

Build a terminal program that:

- asks for the number of players,
- validates that the player count is between 2 and 4,
- lets each player roll during their turn,
- adds roll values to a temporary turn score,
- ends a turn immediately when a player rolls `1`,
- adds the turn score to the player's total score,
- repeats until one player reaches the target score,
- prints the winner and winning score.

## Learning Focus

- `random.randint()` for dice rolls,
- input validation for numeric ranges,
- lists for player scores,
- nested loops,
- turn-based state,
- score accumulation,
- finding the maximum score and winning player.

## Planned Run Command

The exact command will be finalized after the implementation is added. The intended shape is:

```powershell
python projects/06_pig_dice_game/src/pig_dice_game.py
```

## Expected Terminal Interaction

Because dice rolls are random, exact output will vary. A valid run should look like this:

```text
Enter the number of players (2 - 4): 2

Player 1 turn has started.
Your total score is 0.
Would you like to roll? y
You rolled a 5.
Your current turn score is 5.
Would you like to roll? n
Your total score is 5.
```

Invalid player count example:

```text
Enter the number of players (2 - 4): five
Invalid input. Please enter a number.
Enter the number of players (2 - 4): 5
Player count must be between 2 and 4.
Enter the number of players (2 - 4): 2
```

## Completion Checklist

- The game can be run from the terminal.
- Player count input is validated.
- Each player gets a turn.
- Rolling `1` ends the current turn and resets the turn score.
- Choosing not to roll saves the current turn score.
- The game ends when a player reaches the target score.
- The winner is printed clearly.
