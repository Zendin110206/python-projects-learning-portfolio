# Project 11 - WPM Typing Test

Status: In progress.

This project is a terminal-based words-per-minute typing test. It is intended for practicing text loading, real-time keyboard input, terminal display updates, timing, accuracy feedback, and WPM calculation.

## Goal

Build a terminal program that:

- shows a welcome screen,
- loads a random typing prompt from a text file,
- displays the target text,
- captures user keystrokes,
- highlights correct and incorrect characters,
- calculates live words per minute,
- lets the user finish the prompt or exit,
- allows repeated typing rounds.

## Learning Focus

- reading text prompts from a file,
- `curses.wrapper()` for terminal UI setup,
- non-blocking keyboard input,
- terminal color pairs,
- timing with `time.time()`,
- WPM calculation,
- backspace handling,
- separating display logic from calculation logic.

## Planned Run Command

The exact command will be finalized after the implementation is added. The intended shape is:

```powershell
python projects/11_wpm_typing_test/src/wpm_typing_test.py
```

## Expected Terminal Interaction

The program runs inside the terminal. A valid run should show:

```text
Welcome to the WPM Typing Test!
Press any key to begin.
```

During a test, the terminal should show the target text, typed characters, and a live WPM value. Correct characters should be highlighted differently from incorrect characters.

## Completion Checklist

- The program can be run from the terminal.
- Typing prompts are loaded from a text file.
- A random prompt is selected each round.
- WPM is calculated from elapsed time and typed characters.
- Backspace works.
- Incorrect characters are visually marked.
- The user can complete a prompt and start another round.
- The user can exit cleanly.
