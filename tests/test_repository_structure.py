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
        "pyproject.toml",
        "requirements-dev.txt",
    ]

    missing = [path for path in required_paths if not (ROOT / path).is_file()]

    assert missing == []


def test_local_context_is_not_tracked_by_default() -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    assert "/local_context/" in gitignore


def test_public_docs_do_not_expose_private_assistance_workflow() -> None:
    public_docs = [
        ".gitignore",
        "README.md",
        "docs/learning-workflow.md",
        "docs/references.md",
        "projects/README.md",
        "projects/01_quiz_game/README.md",
    ]

    private_term = "".join(["a", "gent"])
    leaked_files = []
    for path in public_docs:
        text = (ROOT / path).read_text(encoding="utf-8").lower()
        if private_term in text:
            leaked_files.append(path)

    assert leaked_files == []
