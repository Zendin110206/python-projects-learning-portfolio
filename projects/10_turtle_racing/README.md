# Project 10 - Turtle Racing

Status: In progress.

This project is a graphical turtle racing simulation. It is intended for practicing Python's `turtle` module, random movement, coordinate-based race logic, and simple visual program structure.

## Goal

Build a program that:

- asks for the number of racers,
- validates that the racer count is within the allowed range,
- creates one turtle per racer,
- spaces racers evenly on the screen,
- moves each racer forward by a random amount,
- stops when a racer reaches the finish line,
- prints the winning racer.

## Learning Focus

- `turtle.Screen()` for the drawing window,
- `turtle.Turtle()` for racer objects,
- screen setup and coordinate positioning,
- random movement with `random.randrange()`,
- lists of racer objects,
- loops for creating and moving racers,
- detecting a winner with turtle coordinates.

## Planned Run Command

The exact command will be finalized after the implementation is added. The intended shape is:

```powershell
python projects/10_turtle_racing/src/turtle_racing.py
```

## Expected Interaction

The program opens a turtle graphics window. A valid run should:

```text
Enter the number of racers (2 - 8): 4
The winner is red!
```

The visual race should show multiple colored turtles moving across the screen until one reaches the finish line.

## Completion Checklist

- The program can be run from the terminal.
- Racer count input is validated.
- Racer colors are assigned clearly.
- Turtles start in evenly spaced positions.
- Each racer moves by a random distance.
- The race stops when a winner reaches the finish line.
- The winner is printed clearly.
