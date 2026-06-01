import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "01_quiz_game" / "src" / "quiz_game.py"


def run_quiz(user_input: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=user_input,
        capture_output=True,
        check=False,
        text=True,
    )


def test_quiz_game_all_answers_correct() -> None:
    result = run_quiz(
        "\n".join(
            [
                "yes",
                "central processing unit",
                "graphics processing unit",
                "random access memory",
                "power supply",
            ]
        )
        + "\n"
    )

    assert result.returncode == 0
    assert "You got 4 questions correct." in result.stdout
    assert "You got 100.0%." in result.stdout


def test_quiz_game_counts_incorrect_answers() -> None:
    result = run_quiz(
        "\n".join(
            [
                "yes",
                "central",
                "graphic processing unit",
                "random access memory",
                "power station unit",
            ]
        )
        + "\n"
    )

    assert result.returncode == 0
    assert "You got 1 questions correct." in result.stdout
    assert "You got 25.0%." in result.stdout


def test_quiz_game_exits_when_player_does_not_choose_yes() -> None:
    result = run_quiz("no\n")

    assert result.returncode == 0
    assert "Maybe next time!" in result.stdout
    assert "What does CPU stand for?" not in result.stdout


def test_quiz_game_accepts_case_and_outer_space_variations() -> None:
    result = run_quiz(
        "\n".join(
            [
                " YES ",
                " Central Processing Unit ",
                " GRAPHICS PROCESSING UNIT ",
                " Random Access Memory ",
                " POWER SUPPLY ",
            ]
        )
        + "\n"
    )

    assert result.returncode == 0
    assert "You got 4 questions correct." in result.stdout
    assert "You got 100.0%." in result.stdout
