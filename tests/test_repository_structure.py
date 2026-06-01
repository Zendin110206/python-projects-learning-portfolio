from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_repository_docs_exist() -> None:
    required_paths = [
        "README.md",
        "PROJECTS.md",
        "docs/learning-workflow.md",
        "docs/references.md",
        "projects/README.md",
        "projects/01_quiz_game/README.md",
        "projects/02_number_guessing_game/README.md",
        "projects/02_number_guessing_game/src/number_guessing_game.py",
        "projects/03_rock_paper_scissors/README.md",
        "projects/03_rock_paper_scissors/src/rock_paper_scissors.py",
        "projects/04_choose_your_own_adventure/README.md",
        "projects/04_choose_your_own_adventure/src/choose_your_own_adventure.py",
        "projects/05_password_manager/README.md",
        "projects/05_password_manager/src/password_manager.py",
        "projects/06_pig_dice_game/README.md",
        "projects/06_pig_dice_game/src/pig_dice_game.py",
        "projects/07_madlibs_generator/README.md",
        "pyproject.toml",
        "requirements-dev.txt",
    ]

    missing = [path for path in required_paths if not (ROOT / path).is_file()]

    assert missing == []


def test_local_notes_are_not_tracked_by_default() -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    ignored_notes_dir = "/" + "local" + "_" + "context" + "/"

    assert ignored_notes_dir in gitignore


def test_public_docs_use_neutral_wording() -> None:
    public_docs = [
        "README.md",
        "docs/learning-workflow.md",
        "docs/references.md",
        "projects/README.md",
        "projects/01_quiz_game/README.md",
        "projects/02_number_guessing_game/README.md",
        "projects/03_rock_paper_scissors/README.md",
        "projects/04_choose_your_own_adventure/README.md",
        "projects/05_password_manager/README.md",
        "projects/06_pig_dice_game/README.md",
        "projects/07_madlibs_generator/README.md",
    ]

    blocked_terms = [
        "".join(["a", "gent"]),
        "local" + "_" + "context",
        "co" + "dex",
    ]
    leaked_files = []
    for path in public_docs:
        text = (ROOT / path).read_text(encoding="utf-8").lower()
        if any(term in text for term in blocked_terms):
            leaked_files.append(path)

    assert leaked_files == []
