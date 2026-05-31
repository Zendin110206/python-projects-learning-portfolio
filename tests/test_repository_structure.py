from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_repository_docs_exist() -> None:
    required_paths = [
        "README.md",
        "PROJECTS.md",
        "docs/learning-workflow.md",
        "docs/references.md",
        "projects/README.md",
        "pyproject.toml",
        "requirements-dev.txt",
    ]

    missing = [path for path in required_paths if not (ROOT / path).is_file()]

    assert missing == []


def test_local_context_is_not_tracked_by_default() -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    assert "/local_context/" in gitignore
