# Python Projects Learning Portfolio

A curated Python learning portfolio focused on small, practical projects, independent implementation, and clear documentation.

This repository is inspired by Tech With Tim's public Python project sequence, but the implementations are intended to be written independently. The goal is to build strong Python fundamentals through deliberate practice, not to copy finished tutorial code.

## Current Status

| Area | Status |
| --- | --- |
| Repository setup | Complete |
| Project 01 - Quiz Game | Complete |
| Project 02 - Number Guessing Game | Complete |
| Project 03 - Rock, Paper, Scissors | Complete |
| Project 04 - Choose Your Own Adventure Game | Complete |
| Project 05 - Password Manager | Complete |
| Project 06 - PIG Dice Game | Complete |
| Project 07 - Mad Libs Generator | Complete |
| Project 08 - Timed Math Challenge | Complete |
| Project 09 - Slot Machine | Complete |
| Project 10 - Turtle Racing | Complete |
| Project 11 - WPM Typing Test | In progress |
| Project implementations | Added one project at a time |

Projects 01 through 10 are implemented and covered by basic automated checks. Project 11 currently has a public project brief and will be implemented manually as the next exercise.

## Learning Goals

- Strengthen Python fundamentals through hands-on projects.
- Practice writing readable command-line programs.
- Build a consistent habit of documenting project scope, behavior, and limitations.
- Use tests and linting where they add meaningful confidence.
- Keep each project honest about its status, scope, and learning purpose.

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── learning-workflow.md
│   └── references.md
├── projects/
│   ├── README.md
│   ├── 01_quiz_game/
│   │   ├── README.md
│   │   └── src/
│   │       └── quiz_game.py
│   ├── 02_number_guessing_game/
│   │   ├── README.md
│   │   └── src/
│   │       └── number_guessing_game.py
│   ├── 03_rock_paper_scissors/
│   │   ├── README.md
│   │   └── src/
│   │       └── rock_paper_scissors.py
│   ├── 04_choose_your_own_adventure/
│   │   ├── README.md
│   │   └── src/
│   │       └── choose_your_own_adventure.py
│   ├── 05_password_manager/
│   │   ├── README.md
│   │   └── src/
│   │       └── password_manager.py
│   ├── 06_pig_dice_game/
│   │   ├── README.md
│   │   └── src/
│   │       └── pig_dice_game.py
│   ├── 07_madlibs_generator/
│   │   ├── README.md
│   │   ├── story.txt
│   │   └── src/
│   │       └── madlibs_generator.py
│   ├── 08_timed_math_challenge/
│   │   ├── README.md
│   │   └── src/
│   │       └── timed_math_challenge.py
│   ├── 09_slot_machine/
│   │   ├── README.md
│   │   └── src/
│   │       └── slot_machine.py
│   ├── 10_turtle_racing/
│   │   ├── README.md
│   │   └── src/
│   │       └── turtle_racing.py
│   └── 11_wpm_typing_test/
│       └── README.md
├── tests/
│   ├── test_project_01_quiz_game.py
│   ├── test_project_02_number_guessing_game.py
│   ├── test_project_03_rock_paper_scissors.py
│   ├── test_project_04_choose_your_own_adventure.py
│   ├── test_project_05_password_manager.py
│   ├── test_project_06_pig_dice_game.py
│   ├── test_project_07_madlibs_generator.py
│   ├── test_project_08_timed_math_challenge.py
│   ├── test_project_09_slot_machine.py
│   ├── test_project_10_turtle_racing.py
│   └── test_repository_structure.py
├── PROJECTS.md
├── pyproject.toml
├── requirements-dev.txt
└── README.md
```

## Getting Started

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Run the repository checks:

```powershell
python -m pytest
python -m ruff check .
```

## Quality Checks

This repository uses:

- `pytest` for automated checks.
- `ruff` for Python linting.
- GitHub Actions for continuous integration on push and pull request events.

The current CI workflow installs the development dependencies, runs the test suite, and checks the code with Ruff.

## Project Roadmap

The full project sequence is tracked in [PROJECTS.md](PROJECTS.md).

Each project should eventually include:

- a concise project README,
- clear input and output behavior,
- source code that can be run from the terminal,
- tests when the logic is deterministic,
- notes about limitations and possible improvements.

## Attribution

This repository is inspired by the project order from Tech With Tim's public Python project tutorial video. It is not affiliated with Tech With Tim. External references are listed in [docs/references.md](docs/references.md).
