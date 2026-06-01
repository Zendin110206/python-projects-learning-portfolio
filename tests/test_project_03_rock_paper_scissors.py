import io
import runpy
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "03_rock_paper_scissors" / "src" / "rock_paper_scissors.py"


def run_game(
    player_inputs: list[str],
    computer_choices: list[str] | None = None,
) -> str:
    inputs = iter(player_inputs)
    choices = iter(computer_choices or [])
    output = io.StringIO()

    def fake_input(prompt: str) -> str:
        print(prompt, end="")
        return next(inputs)

    def fake_choice(options: list[str]) -> str:
        return next(choices)

    with (
        patch("builtins.input", fake_input),
        patch("random.choice", fake_choice),
        redirect_stdout(output),
    ):
        runpy.run_path(str(SCRIPT), run_name="__main__")

    return output.getvalue()


def test_rock_paper_scissors_quits_with_zero_score() -> None:
    output = run_game(["q"])

    assert "You won 0 times." in output
    assert "The computer won 0 times." in output
    assert "Goodbye!" in output
    assert "Computer picked" not in output


def test_rock_paper_scissors_rejects_invalid_input_without_score_change() -> None:
    output = run_game(["banana", "q"])

    assert "Please type rock, paper, scissors, or q." in output
    assert "You won 0 times." in output
    assert "The computer won 0 times." in output
    assert "Computer picked" not in output


def test_rock_paper_scissors_accepts_normalized_player_input() -> None:
    output = run_game([" ROCK ", "q"], ["scissors"])

    assert "Please type rock, paper, scissors, or q." not in output
    assert "Computer picked scissors." in output
    assert "You won!" in output
    assert "You won 1 times." in output
    assert "The computer won 0 times." in output


def test_rock_paper_scissors_tracks_computer_win() -> None:
    output = run_game(["rock", "q"], ["paper"])

    assert "Computer picked paper." in output
    assert "You lost!" in output
    assert "You won 0 times." in output
    assert "The computer won 1 times." in output


def test_rock_paper_scissors_handles_tie_without_changing_score() -> None:
    output = run_game(["scissors", "q"], ["scissors"])

    assert "Computer picked scissors." in output
    assert "It's a tie!" in output
    assert "You won 0 times." in output
    assert "The computer won 0 times." in output
