import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "02_number_guessing_game" / "src" / "number_guessing_game.py"


def run_number_guessing_game(user_input: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=user_input,
        capture_output=True,
        check=False,
        text=True,
    )


def test_number_guessing_game_rejects_non_numeric_upper_bound() -> None:
    result = run_number_guessing_game("abc\n")

    assert result.returncode == 0
    assert "Please type a number next time." in result.stdout
    assert "Traceback" not in result.stderr


def test_number_guessing_game_rejects_zero_upper_bound_without_crashing() -> None:
    result = run_number_guessing_game("0\n")

    assert result.returncode == 0
    assert "Please type a number" in result.stdout
    assert "Traceback" not in result.stderr


def test_number_guessing_game_can_be_won_with_one_possible_number() -> None:
    result = run_number_guessing_game("1\n1\n")

    assert result.returncode == 0
    assert "You got it!" in result.stdout
    assert "1 guesses" in result.stdout


def test_number_guessing_game_does_not_count_invalid_guess() -> None:
    result = run_number_guessing_game("1\nabc\n1\n")

    assert result.returncode == 0
    assert "Please type a number next time." in result.stdout
    assert "You got it!" in result.stdout
    assert "1 guesses" in result.stdout
