import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "projects"
    / "08_timed_math_challenge"
    / "src"
    / "timed_math_challenge.py"
)


def load_timed_math_challenge() -> ModuleType:
    spec = importlib.util.spec_from_file_location("timed_math_challenge_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def run_with_inputs(function, player_inputs: list[str], *args) -> str:
    _, output = call_with_inputs(function, player_inputs, *args)

    return output


def call_with_inputs(function, player_inputs: list[str], *args):
    inputs = iter(player_inputs)
    output = io.StringIO()

    def fake_input(prompt: str = "") -> str:
        print(prompt, end="")
        return next(inputs)

    with patch("builtins.input", fake_input), redirect_stdout(output):
        result = function(*args)

    return result, output.getvalue()


def test_calculate_answer_supports_all_operators() -> None:
    timed_math_challenge = load_timed_math_challenge()

    assert timed_math_challenge.calculate_answer(
        left_operand=8,
        right_operand=4,
        operator="+",
    ) == 12
    assert timed_math_challenge.calculate_answer(
        left_operand=8,
        right_operand=4,
        operator="-",
    ) == 4
    assert timed_math_challenge.calculate_answer(
        left_operand=8,
        right_operand=4,
        operator="*",
    ) == 32


def test_calculate_answer_rejects_unknown_operator() -> None:
    timed_math_challenge = load_timed_math_challenge()

    with pytest.raises(ValueError, match="Unsupported operator"):
        timed_math_challenge.calculate_answer(
            left_operand=8,
            right_operand=4,
            operator="/",
        )


def test_generate_problem_builds_expression_and_answer() -> None:
    timed_math_challenge = load_timed_math_challenge()

    with (
        patch.object(timed_math_challenge.rd, "randint", side_effect=[8, 4]),
        patch.object(timed_math_challenge.rd, "choice", return_value="+"),
    ):
        expression, answer = timed_math_challenge.generate_problem()

    assert expression == "8 + 4"
    assert answer == 12


def test_run_challenge_retries_wrong_answers_and_counts_attempts() -> None:
    timed_math_challenge = load_timed_math_challenge()

    with (
        patch.object(timed_math_challenge, "TOTAL_PROBLEMS", 2),
        patch.object(
            timed_math_challenge,
            "generate_problem",
            side_effect=[("8 + 4", 12), ("9 * 3", 27)],
        ),
    ):
        wrong_attempts, output = call_with_inputs(
            timed_math_challenge.run_challenge,
            ["11", "12", "abc", "27"],
        )

    assert output.count("Problem #1: 8 + 4 = ") == 2
    assert output.count("Problem #2: 9 * 3 = ") == 2
    assert wrong_attempts == 2


def test_run_challenge_returns_wrong_attempt_count() -> None:
    timed_math_challenge = load_timed_math_challenge()

    with (
        patch.object(timed_math_challenge, "TOTAL_PROBLEMS", 1),
        patch.object(timed_math_challenge, "generate_problem", return_value=("5 * 6", 30)),
    ):
        wrong_attempts, output = call_with_inputs(
            timed_math_challenge.run_challenge,
            ["29", "abc", "30"],
        )

    assert output.count("Problem #1: 5 * 6 = ") == 3
    assert wrong_attempts == 2


def test_main_prints_timer_summary() -> None:
    timed_math_challenge = load_timed_math_challenge()

    with (
        patch.object(timed_math_challenge, "run_challenge", return_value=2),
        patch.object(timed_math_challenge.time, "time", side_effect=[10.0, 34.19]),
    ):
        output = run_with_inputs(timed_math_challenge.main, [""])

    assert "Press enter to start." in output
    assert "----------------------" in output
    assert "Nice work! You finished in 24.19 seconds." in output
    assert "You made 2 incorrect attempts." in output
