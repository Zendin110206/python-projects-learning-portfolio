# Project 16 - Currency Converter

Status: In progress.

This project is a command-line currency converter. It is intended for practicing dictionary-based lookup, decimal arithmetic, input validation, menu commands, and clear terminal formatting.

## Goal

Build a terminal program that:

- shows a simple command menu,
- lists supported currencies,
- converts an amount from one currency to another,
- shows an exchange rate between two currencies,
- validates currency codes and amounts,
- exits cleanly.

## Learning Focus

- storing rates in dictionaries,
- validating command input,
- normalizing currency codes,
- using `Decimal` for money values,
- formatting converted amounts,
- keeping conversion logic separate from terminal interaction.

## Planned Run Command

The exact command will be finalized after the implementation is added. The intended shape is:

```powershell
python projects/16_currency_converter/src/currency_converter.py
```

## Expected Terminal Behavior

A valid run should show commands for:

- listing supported currencies,
- converting an amount,
- checking a rate,
- quitting the program.

Invalid commands, currency codes, and amounts should be rejected with clear messages.

## Completion Checklist

- The program can be run from the terminal.
- Supported currencies can be listed.
- Currency codes are validated.
- Amount input is validated as a positive finite number.
- Conversion uses decimal arithmetic.
- Exchange rates are calculated correctly from the local rate table.
- Formatting and conversion logic are covered by tests where practical.

## Notes

- The first version uses a local exchange-rate table so the exercise remains stable and repeatable.
- Live exchange-rate APIs can be explored later as an optional improvement.
