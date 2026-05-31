# Learning Workflow

This repository is designed for independent practice. The agent may prepare problem briefs, quality gates, and review notes, but the project code should be written manually by the learner.

## Workflow

1. Read the project brief.
2. Restate the expected input, output, and rules.
3. Plan the smallest working version.
4. Implement the project manually.
5. Run the project from the terminal.
6. Add tests for deterministic logic.
7. Review readability, naming, edge cases, and documentation.
8. Commit the completed checkpoint.

## Agent Boundary

The agent may:

- Explain concepts in Indonesian when needed.
- Prepare markdown guidance in `local_context/`.
- Review code and point out bugs.
- Suggest tests and edge cases.
- Help verify commands and repository health.

The agent should avoid:

- Writing the full project solution before the learner tries.
- Turning beginner projects into unnecessarily abstract architecture.
- Adding public claims that make a learning project sound production-grade.

## Public Documentation Standard

Public repository files should stay professional and concise. They should explain what the project does, how to run it, what was learned, and what limitations remain.
