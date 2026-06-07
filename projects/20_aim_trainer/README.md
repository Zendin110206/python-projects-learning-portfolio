# Project 20 - Aim Trainer

Status: Completed.

This project is a Pygame-based aim trainer. It is intended for practicing graphical game loops, timed target spawning, mouse collision detection, animated targets, live performance metrics, and an end screen.

## Goal

Build a desktop game that:

- opens a Pygame window,
- spawns targets on a timed interval,
- animates targets as they grow and shrink,
- lets the player click targets with the mouse,
- tracks hits, misses, lives, elapsed time, speed, and accuracy,
- ends when the player runs out of lives.

## Learning Focus

- setting up a Pygame window,
- using a game loop with `pygame.time.Clock`,
- drawing circles and rectangles,
- handling `QUIT`, timer, and mouse events,
- calculating circle collision with distance math,
- rendering text labels,
- separating target behavior, drawing, metrics, and loop control.

## Run Command

From the repository root:

```powershell
python projects/20_aim_trainer/src/aim_trainer.py
```

## Expected Runtime Behavior

A valid run should open a window titled `Aim Trainer`, spawn animated targets, update the top metrics bar, and show a final results screen when the player runs out of lives.

## Completion Checklist

- The game can be run from the terminal.
- The Pygame window opens with the expected title and size.
- Targets spawn inside the playable area.
- Targets grow, shrink, and disappear when missed.
- Mouse clicks remove targets when they collide.
- Misses reduce remaining lives.
- The top bar shows time, speed, hits, and lives.
- The end screen shows time, speed, hits, and accuracy.
- Core math and formatting logic is covered by tests where practical.

## Notes

- This project uses `pygame`.
- Automated tests should focus on pure logic, formatting, target collision, and event-independent behavior.
- Manual visual testing is required for the game window and interaction.
- Automated tests cover timing helpers, target growth, collision, random spawn bounds, and top-bar label text.
