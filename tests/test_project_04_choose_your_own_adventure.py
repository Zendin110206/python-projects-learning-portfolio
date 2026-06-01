import io
import runpy
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "projects"
    / "04_choose_your_own_adventure"
    / "src"
    / "choose_your_own_adventure.py"
)


def run_adventure(player_inputs: list[str]) -> str:
    inputs = iter(player_inputs)
    output = io.StringIO()

    def fake_input(prompt: str) -> str:
        print(prompt, end="")
        return next(inputs)

    with patch("builtins.input", fake_input), redirect_stdout(output):
        runpy.run_path(str(SCRIPT), run_name="__main__")

    return output.getvalue()


def test_adventure_left_swim_path_loses() -> None:
    output = run_adventure(["Alex", "left", "swim"])

    assert "Welcome Alex to this adventure!" in output
    assert "You swam across and were eaten by an alligator." in output
    assert "Thank you for trying, Alex." in output


def test_adventure_left_walk_path_loses() -> None:
    output = run_adventure(["Alex", "left", "walk"])

    assert "You walked for many miles, ran out of water, and lost." in output
    assert "Thank you for trying, Alex." in output


def test_adventure_invalid_river_choice_loses() -> None:
    output = run_adventure(["Alex", "left", "jump"])

    assert "Not a valid option. You lose." in output
    assert "Thank you for trying, Alex." in output


def test_adventure_right_back_path_loses() -> None:
    output = run_adventure(["Alex", "right", "back"])

    assert "You go back and lose." in output
    assert "Thank you for trying, Alex." in output


def test_adventure_right_cross_yes_path_wins() -> None:
    output = run_adventure(["Alex", "right", "cross", "yes"])

    assert "You cross the bridge and meet a stranger." in output
    assert "You talk to the stranger and they give you gold. You win!" in output
    assert "Thank you for trying, Alex." in output


def test_adventure_right_cross_no_path_loses() -> None:
    output = run_adventure(["Alex", "right", "cross", "no"])

    assert "You ignore the stranger and they are offended. You lose." in output
    assert "Thank you for trying, Alex." in output


def test_adventure_invalid_start_choice_loses() -> None:
    output = run_adventure(["Alex", "middle"])

    assert "Not a valid option. You lose." in output
    assert "Thank you for trying, Alex." in output


def test_adventure_accepts_case_and_outer_space_variations() -> None:
    output = run_adventure(["Alex", " RIGHT ", " Cross ", " YES "])

    assert "Not a valid option. You lose." not in output
    assert "You talk to the stranger and they give you gold. You win!" in output
