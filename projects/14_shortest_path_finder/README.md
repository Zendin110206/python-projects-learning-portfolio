# Project 14 - Shortest Path Finder

Status: Completed.

This project is a terminal-based shortest path finder. It is intended for practicing grid traversal, breadth-first search, queues, coordinate handling, and terminal visualization.

## Goal

Build a terminal program that:

- represents a maze as a two-dimensional grid,
- finds the start and end positions,
- explores valid neighboring cells,
- avoids walls and previously visited positions,
- uses breadth-first search to find the shortest path in an unweighted maze,
- visualizes the search and final path clearly in the terminal.

## Learning Focus

- grid-based data structures,
- row and column coordinates,
- `queue.Queue()` for first-in, first-out traversal,
- visited sets,
- path reconstruction with lists of coordinates,
- `curses`-based terminal drawing,
- keeping visualization code separate from pathfinding logic where practical.

## Run Command

From the repository root:

```powershell
python projects/14_shortest_path_finder/src/shortest_path_finder.py
```

## Expected Terminal Behavior

The program should open a terminal-based maze display. A valid run should:

- show a maze with walls, a start point, and an end point,
- animate the search as it explores cells,
- highlight the shortest path when the end point is found,
- wait for one key press before closing.

## Completion Checklist

- The program can be run from the terminal.
- The maze contains one start point and one end point.
- Wall cells are never added to the path.
- Already visited cells are not explored repeatedly.
- Breadth-first search returns the shortest path for the static maze.
- Terminal drawing is clear and does not run on import.
- Deterministic logic is covered by tests where practical.

## Notes

- The first version uses a static maze.
- The first version is terminal-only and does not include a maze editor.
- Breadth-first search is appropriate here because every valid move has equal cost.
- The terminal window waits for a key press before closing after the search finishes.
