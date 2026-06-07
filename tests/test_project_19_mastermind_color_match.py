import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "projects"
    / "19_mastermind_color_match"
    / "src"
    / "mastermind_color_match.py"
)


def load_mastermind_color_match() -> ModuleType:
    spec = importlib.util.spec_from_file_location("mastermind_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def call_with_inputs(function, player_inputs: list[str]):
    inputs = iter(player_inputs)
    output = io.StringIO()

    def fake_input(prompt: str = "") -> str:
        print(prompt, end="")
        return next(inputs)

    with patch("builtins.input", fake_input), redirect_stdout(output):
        result = function()

    return result, output.getvalue()


def test_module_import_does_not_prompt_or_generate_secret() -> None:
    with (
        patch("builtins.input") as input_mock,
        patch("random.choices") as choices,
    ):
        load_mastermind_color_match()

    input_mock.assert_not_called()
    choices.assert_not_called()


def test_generate_secret_code_uses_four_valid_colors() -> None:
    mastermind = load_mastermind_color_match()

    with patch.object(mastermind.rd, "choices", return_value=["R", "G", "B", "Y"]) as choices:
        secret_code = mastermind.generate_secret_code()

    assert secret_code == ["R", "G", "B", "Y"]
    choices.assert_called_once_with(mastermind.VALID_COLORS, k=mastermind.CODE_LENGTH)


def test_format_helpers_return_expected_text() -> None:
    mastermind = load_mastermind_color_match()

    assert mastermind.format_secret_code(["R", "G", "B", "Y"]) == "R G B Y"
    assert mastermind.format_valid_colors() == (
        "R=Red, G=Green, B=Blue, Y=Yellow, W=White, P=Purple"
    )


def test_parse_guess_normalizes_input_and_handles_quit() -> None:
    mastermind = load_mastermind_color_match()

    assert mastermind.parse_guess(" r g b y ") == ["R", "G", "B", "Y"]
    assert mastermind.parse_guess("RGBY") == ["RGBY"]
    assert mastermind.parse_guess("q") == "quit"
    assert mastermind.parse_guess(" Q ") == "quit"


def test_validate_guess_reports_length_color_and_valid_states() -> None:
    mastermind = load_mastermind_color_match()

    assert mastermind.validate_guess(["R", "G", "B", "Y"]) == "valid"
    assert mastermind.validate_guess(["R", "G", "B"]) == "invalid_length"
    assert mastermind.validate_guess(["R", "G", "B", "Y", "W"]) == "invalid_length"
    assert mastermind.validate_guess(["R", "G", "B", "X"]) == "invalid_color"


def test_score_guess_handles_exact_color_only_and_duplicates() -> None:
    mastermind = load_mastermind_color_match()

    assert mastermind.score_guess(["R", "G", "B", "Y"], ["R", "B", "G", "Y"]) == (2, 2)
    assert mastermind.score_guess(["R", "R", "G", "B"], ["R", "R", "R", "R"]) == (2, 0)
    assert mastermind.score_guess(["R", "R", "G", "B"], ["R", "G", "R", "Y"]) == (1, 2)
    assert mastermind.score_guess(["B", "B", "Y", "P"], ["B", "Y", "B", "B"]) == (1, 2)
    assert mastermind.score_guess(["G", "P", "W", "R"], ["R", "W", "P", "G"]) == (0, 4)


def test_print_intro_uses_exact_opening_text() -> None:
    mastermind = load_mastermind_color_match()
    output = io.StringIO()

    with redirect_stdout(output):
        mastermind.print_intro()

    assert output.getvalue() == (
        "Mastermind - 4 Color Match\n"
        "Valid colors: R=Red, G=Green, B=Blue, Y=Yellow, W=White, P=Purple\n"
        "Guess the 4-color secret code. Duplicates are allowed.\n"
        "You have 10 attempts.\n"
    )


def test_play_game_handles_quit_and_reveals_secret() -> None:
    mastermind = load_mastermind_color_match()

    with patch.object(mastermind, "generate_secret_code", return_value=["R", "G", "B", "Y"]):
        _, output = call_with_inputs(mastermind.play_game, ["q"])

    assert "Enter guess #1: Game ended. Secret code was: R G B Y" in output


def test_play_game_does_not_count_invalid_guesses_as_attempts() -> None:
    mastermind = load_mastermind_color_match()

    with patch.object(mastermind, "generate_secret_code", return_value=["R", "G", "B", "Y"]):
        _, output = call_with_inputs(
            mastermind.play_game,
            ["R G B", "R G B X", "R G B Y"],
        )

    assert output.count("Enter guess #1:") == 3
    assert "Enter exactly 4 colors." in output
    assert "Use only valid color codes: R, G, B, Y, W, P." in output
    assert "You cracked the code in 1 attempts." in output


def test_play_game_shows_score_before_win_message() -> None:
    mastermind = load_mastermind_color_match()

    with patch.object(mastermind, "generate_secret_code", return_value=["R", "G", "B", "Y"]):
        _, output = call_with_inputs(mastermind.play_game, ["R G B Y"])

    assert output.index("Exact matches: 4") < output.index("You cracked the code")
    assert "Color-only matches: 0" in output
    assert "You cracked the code in 1 attempts." in output


def test_play_game_shows_out_of_attempts_after_ten_valid_wrong_guesses() -> None:
    mastermind = load_mastermind_color_match()
    wrong_guesses = ["R R R R"] * mastermind.MAX_ATTEMPTS

    with patch.object(mastermind, "generate_secret_code", return_value=["G", "G", "G", "G"]):
        _, output = call_with_inputs(mastermind.play_game, wrong_guesses)

    assert "Enter guess #10:" in output
    assert output.rstrip().endswith("Out of attempts. Secret code was: G G G G")
