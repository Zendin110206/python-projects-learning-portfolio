# Project 16 - Currency Converter

Status: Completed.

This project is a command-line currency converter. It is intended for practicing API requests, JSON parsing, decimal arithmetic, input validation, menu commands, and clear terminal formatting.

## Goal

Build a terminal program that:

- shows a simple command menu,
- fetches supported currencies from a public exchange-rate API,
- converts an amount from one currency to another,
- shows an exchange rate between two currencies,
- validates currency codes and amounts,
- handles API failures clearly,
- exits cleanly.

## Learning Focus

- making HTTP GET requests with `requests`,
- parsing JSON API responses,
- validating command input,
- normalizing currency codes,
- using `Decimal` for money values,
- formatting converted amounts,
- keeping API, conversion, and terminal logic separate.

## Run Command

From the repository root:

```powershell
python projects/16_currency_converter/src/currency_converter.py
```

## Expected Terminal Behavior

A valid run should show commands for:

- listing supported currencies,
- converting an amount,
- checking a rate,
- quitting the program.

Invalid commands, currency codes, amounts, and API failures should be handled with clear messages.

## Completion Checklist

- The program can be run from the terminal.
- Supported currencies can be fetched and listed.
- Currency codes are validated.
- Amount input is validated as a positive finite number.
- Conversion uses decimal arithmetic.
- Exchange rates are fetched from the API and parsed correctly.
- API failures are handled without tracebacks.
- Formatting and parsing logic are covered by tests where practical.

## Notes

- The first version uses the Frankfurter exchange-rate API, which does not require an API key.
- Automated tests should mock API responses so the test suite remains stable.
- API failures are handled with a clear terminal message instead of a traceback.
