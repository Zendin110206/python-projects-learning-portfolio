# Project 04 - Choose Your Own Adventure Game

Status: Completed.

This project is a beginner-friendly command-line adventure game. The player enters a name, makes story choices, and reaches a win, loss, or invalid-choice ending.

## Goal

Build a small terminal program that:

- asks the player for their name,
- welcomes the player into a short text adventure,
- presents story choices,
- reads and normalizes the player's choices,
- branches into different story paths,
- handles invalid choices clearly,
- ends with a win or loss outcome,
- prints a closing message.

## Learning Focus

- collecting text input,
- normalizing player choices,
- nested conditional logic,
- story branching,
- readable terminal output,
- keeping control flow clear as choices split into paths.

## Run Command

From the repository root:

```powershell
python projects/04_choose_your_own_adventure/src/choose_your_own_adventure.py
```

## Expected Terminal Interaction

The exact story text may vary, but a valid run should look like this:

```text
Type your name: Alex
Welcome Alex to this adventure!
You are on a dirt road. It has come to an end and you can go left or right.
Which way would you like to go? left
You come to a river. You can walk around it or swim across.
Type walk to walk around and swim to swim across: swim
You swam across and were eaten by an alligator.
Thank you for trying, Alex.
```

Invalid choice example:

```text
Type your name: Alex
Welcome Alex to this adventure!
You are on a dirt road. It has come to an end and you can go left or right.
Which way would you like to go? middle
Not a valid option. You lose.
Thank you for trying, Alex.
```

## Completion Checklist

- The game can be run from the terminal.
- The player is asked for their name.
- The player can choose between at least two starting paths.
- Each path has at least one follow-up choice.
- Invalid choices are handled without crashing.
- The story has clear win and loss endings.
- The final closing message includes the player's name.

## Notes

- User choices are normalized with outer-space trimming and lowercase conversion.
- The story is intentionally short so the project can focus on branching control flow.
- This is a terminal learning project, not a full interactive fiction engine.
