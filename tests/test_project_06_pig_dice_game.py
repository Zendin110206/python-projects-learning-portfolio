import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "06_pig_dice_game" / "src" / "pig_dice_game.py"


def load_pig_dice_game() -> ModuleType:
    spec = importlib.util.spec_from_file_location("pig_dice_game_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def run_with_inputs(function, player_inputs: list[str], *args) -> str:
    inputs = iter(player_inputs)
    output = io.StringIO()

    def fake_input(prompt: str) -> str:
        print(prompt, end="")
        return next(inputs)

    with patch("builtins.input", fake_input), redirect_stdout(output):
        function(*args)

    return output.getvalue()


def test_pig_dice_game_rejects_invalid_player_counts() -> None:
    pig_dice_game = load_pig_dice_game()

    output = io.StringIO()
    inputs = iter(["abc", "1", "5", "2"])

    def fake_input(prompt: str) -> str:
        print(prompt, end="")
        return next(inputs)

    with patch("builtins.input", fake_input), redirect_stdout(output):
        player_count = pig_dice_game.get_player_count()

    assert player_count == 2
    assert "Invalid input. Please enter a number." in output.getvalue()
    assert output.getvalue().count("Player count must be between 2 and 4.") == 2


def test_pig_dice_game_roll_die_uses_one_to_six_range() -> None:
    pig_dice_game = load_pig_dice_game()

    with patch.object(pig_dice_game.rd, "randint", return_value=4) as randint:
        roll_value = pig_dice_game.roll_die()

    assert roll_value == 4
    randint.assert_called_once_with(1, 6)


def test_pig_dice_game_roll_one_ends_turn_with_no_points() -> None:
    pig_dice_game = load_pig_dice_game()
    pig_dice_game.target_score = 5
    roll_values = iter([1, 6])

    with patch.object(pig_dice_game, "roll_die", lambda: next(roll_values)):
        output = run_with_inputs(pig_dice_game.main, ["2", "y", "y"])

    assert "You rolled a 1. Turn over with no points." in output
    assert "Your total score is 0." in output
    assert "Player 2 wins with a score of 6!" in output


def test_pig_dice_game_saves_turn_score_when_player_stops() -> None:
    pig_dice_game = load_pig_dice_game()
    pig_dice_game.target_score = 5
    roll_values = iter([3, 5])

    with patch.object(pig_dice_game, "roll_die", lambda: next(roll_values)):
        output = run_with_inputs(pig_dice_game.main, ["2", "y", "n", "y"])

    assert "You rolled a 3." in output
    assert "Your current turn score is 3." in output
    assert "Your total score is 3." in output
    assert "Player 2 wins with a score of 5!" in output


def test_pig_dice_game_accepts_normalized_roll_input() -> None:
    pig_dice_game = load_pig_dice_game()
    pig_dice_game.target_score = 5

    with patch.object(pig_dice_game, "roll_die", lambda: 5):
        output = run_with_inputs(pig_dice_game.main, ["2", " Y "])

    assert "You rolled a 5." in output
    assert "Player 1 wins with a score of 5!" in output
