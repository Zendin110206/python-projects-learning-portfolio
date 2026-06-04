# Project 15 - Expense Tracker

Status: Completed.

This project is a command-line expense tracker. It is intended for practicing file I/O, CSV data storage, input validation, date handling, numeric parsing, and summary reporting.

## Goal

Build a terminal program that:

- shows a simple menu,
- adds expense records,
- validates date, category, description, and amount input,
- stores records in a CSV file,
- lists saved expenses,
- summarizes total spending by category,
- exits cleanly.

## Learning Focus

- working with CSV files,
- validating structured input,
- parsing dates with `datetime`,
- parsing decimal amounts,
- using `pathlib` for project-relative file paths,
- aggregating records by category,
- keeping storage, formatting, and menu logic readable.

## Run Command

From the repository root:

```powershell
python projects/15_expense_tracker/src/expense_tracker.py
```

## Expected Terminal Behavior

A valid run should show a small menu with options for:

- adding an expense,
- listing expenses,
- showing totals by category,
- exiting the program.

Invalid input should be rejected with clear messages, and the program should not crash when the data file does not exist yet.

## Completion Checklist

- The program can be run from the terminal.
- Menu input is validated.
- Expense dates are validated.
- Expense amounts are validated as positive numbers.
- Expense records are saved to a CSV file.
- Existing records can be listed.
- Totals by category are calculated correctly.
- File and formatting logic is covered by tests where practical.

## Notes

- The first version uses local CSV storage only.
- Runtime data files should stay out of version control.
- This project intentionally avoids live APIs so the exercise remains stable and repeatable.
- The CSV file is created locally at runtime when the program starts.
