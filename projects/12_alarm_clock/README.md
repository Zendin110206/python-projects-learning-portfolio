# Project 12 - Alarm Clock

Status: Completed.

This project is a command-line alarm clock. It is intended for practicing time parsing, input validation, countdown logic, and clear terminal feedback.

## Goal

Build a terminal program that:

- asks the user for an alarm duration,
- validates hour, minute, and second input,
- converts the duration to total seconds,
- counts down until the alarm time is reached,
- prints the remaining time clearly,
- prints a final alarm message when the countdown finishes.

## Learning Focus

- parsing structured time input,
- validating numeric time parts,
- converting hours, minutes, and seconds into total seconds,
- `time.sleep()` for countdown timing,
- loop-based countdown output,
- formatting seconds as `HH:MM:SS`,
- keeping terminal output understandable.

## Run Command

From the repository root:

```powershell
python projects/12_alarm_clock/src/alarm_clock.py
```

## Expected Terminal Interaction

A valid run should look like this:

```text
Enter alarm duration (HH:MM:SS): 00:00:05
Alarm set for 00:00:05.
Time remaining: 00:00:05
Time remaining: 00:00:04
Time remaining: 00:00:03
Time remaining: 00:00:02
Time remaining: 00:00:01
Wake up! Alarm finished.
```

## Completion Checklist

- The program can be run from the terminal.
- Alarm duration input is validated.
- Invalid formats are rejected clearly.
- The duration is converted to total seconds.
- Remaining time is formatted as `HH:MM:SS`.
- The countdown updates once per second.
- A clear final alarm message is printed.

## Notes

- Alarm input represents a duration, not a specific clock time.
- The countdown displays remaining time from the selected duration down to one second.
- The implementation is intentionally terminal-only for the first version.
