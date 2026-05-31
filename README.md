# Python Projects Learning Portfolio

A self-directed Python learning portfolio built around small projects, practical problem solving, and clear documentation. The repository is inspired by Tech With Tim's "9 HOURS of Python Projects - From Beginner to Advanced" project sequence, but the implementations are intended to be written independently as learning exercises.

## Current Status

Repository preparation is complete. Project implementation has not started yet.

The purpose of this initial setup is to create a clean public workspace before the first project begins. Each project will be added one at a time with its own problem brief, implementation, run instructions, and quality checks.

## Learning Principles

- Write the project code independently instead of copying a finished solution.
- Work on one project at a time.
- Keep public documentation in English.
- Keep private learning guidance and agent discussion in `local_context/`.
- Use tests where they add meaningful confidence.
- Keep claims honest: this is a learning portfolio, not a production software suite.

## Repository Structure

```text
.
├── docs/
│   ├── learning-workflow.md
│   └── references.md
├── projects/
│   └── README.md
├── tests/
│   └── test_repository_structure.py
├── PROJECTS.md
├── pyproject.toml
├── requirements-dev.txt
└── README.md
```

`local_context/` exists locally for private planning notes, reading audits, and project guidance. It is intentionally excluded from Git.

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

## Project Roadmap

The planned project sequence is listed in [PROJECTS.md](PROJECTS.md). Each project will be introduced only when it is ready to be worked on, so the repository can grow through deliberate checkpoints instead of unfinished clutter.

## Attribution

This repository is inspired by the project order from Tech With Tim's public Python project tutorial video. It is not affiliated with Tech With Tim, and the goal is not to copy the tutorial source code. The goal is to practice Python by solving each project independently and documenting the learning process professionally.
