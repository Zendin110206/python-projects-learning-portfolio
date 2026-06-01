# Project 04 - Choose Your Own Adventure Game

Status: In progress.

This project is a beginner-friendly command-line adventure game. The implementation is intentionally not included yet because the project is meant to be written independently as Python practice.

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

## Planned Run Command

The exact command will be finalized after the implementation is added. The intended shape is:

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
