# Project 15 - NBA Stats and Current Scores

Status: In progress.

This project is a command-line NBA scoreboard and team statistics viewer. It is intended for practicing API client usage, nested data parsing, sorting, error handling, and clear terminal formatting.

## Goal

Build a terminal program that:

- shows a simple menu,
- fetches current NBA scoreboard data,
- formats game matchups and scores clearly,
- fetches team statistics for a selected season,
- displays the top teams by points per game,
- handles unavailable live data gracefully.

## Learning Focus

- working with third-party API clients,
- parsing nested dictionaries and lists,
- formatting live sports data for terminal output,
- sorting records by numeric values,
- separating data-fetching logic from formatting logic,
- handling network and API failures without crashing.

## Planned Run Command

The exact command will be finalized after the implementation is added. The intended shape is:

```powershell
python projects/15_nba_stats_current_scores/src/nba_stats_current_scores.py
```

## Expected Terminal Behavior

A valid run should show a small menu with options for:

- today's NBA scores,
- top team points per game,
- exit.

If live NBA data is unavailable, the program should show a clear error message instead of a traceback.

## Completion Checklist

- The program can be run from the terminal.
- Menu input is validated.
- Current scores are formatted consistently.
- Team statistics are sorted by points per game.
- Network/API failures are handled clearly.
- Data formatting logic is covered by tests using sample data.

## Notes

- The first version uses `nba_api` as the NBA.com API client.
- Automated tests should avoid live network calls by using sample data or mocks.
- Live scores depend on NBA data availability at runtime.
