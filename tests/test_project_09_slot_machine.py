import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "09_slot_machine" / "src" / "slot_machine.py"


def load_slot_machine() -> ModuleType:
    spec = importlib.util.spec_from_file_location("slot_machine_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def call_with_inputs(function, player_inputs: list[str], *args):
    inputs = iter(player_inputs)
    output = io.StringIO()

    def fake_input(prompt: str = "") -> str:
        print(prompt, end="")
        return next(inputs)

    with patch("builtins.input", fake_input), redirect_stdout(output):
        result = function(*args)

    return result, output.getvalue()


def run_with_inputs(function, player_inputs: list[str], *args) -> str:
    _, output = call_with_inputs(function, player_inputs, *args)

    return output


def test_deposit_money_retries_until_positive_number() -> None:
    slot_machine = load_slot_machine()

    deposit, output = call_with_inputs(
        slot_machine.deposit_money,
        ["abc", "0", "100"],
    )

    assert deposit == 100
    assert "Please enter a number." in output
    assert "Amount must be greater than 0." in output


def test_get_number_of_lines_retries_until_valid_range() -> None:
    slot_machine = load_slot_machine()

    lines, output = call_with_inputs(
        slot_machine.get_number_of_lines,
        ["five", "4", "2"],
    )

    assert lines == 2
    assert output.count("Enter a valid number of lines.") == 2


def test_get_bet_retries_until_valid_range() -> None:
    slot_machine = load_slot_machine()

    bet, output = call_with_inputs(slot_machine.get_bet, ["abc", "0", "101", "5"])

    assert bet == 5
    assert "Please enter a number." in output
    assert output.count("Amount must be between $1 and $100.") == 2


def test_get_slot_machine_spin_returns_rows() -> None:
    slot_machine = load_slot_machine()

    with patch.object(
        slot_machine.rd,
        "choice",
        side_effect=["A", "B", "C", "A", "B", "C", "A", "B", "C"],
    ):
        slots = slot_machine.get_slot_machine_spin(
            rows=3,
            cols=3,
            symbols={"A": 2, "B": 4, "C": 6},
        )

    assert slots == [
        ["A", "A", "A"],
        ["B", "B", "B"],
        ["C", "C", "C"],
    ]


def test_print_slot_machine_formats_rows() -> None:
    slot_machine = load_slot_machine()
    slots = [
        ["A", "B", "D"],
        ["C", "C", "C"],
        ["B", "D", "A"],
    ]

    output = run_with_inputs(slot_machine.print_slot_machine, [], slots)

    assert output == "A | B | D\nC | C | C\nB | D | A\n"


def test_check_winnings_only_counts_selected_lines() -> None:
    slot_machine = load_slot_machine()
    slots = [
        ["A", "A", "A"],
        ["B", "C", "B"],
        ["D", "D", "D"],
    ]

    winnings, winning_lines = slot_machine.check_winnings(
        slots,
        lines=2,
        bet=10,
        values=slot_machine.SYMBOL_VALUE,
    )

    assert winnings == 50
    assert winning_lines == [1]


def test_run_spin_retries_when_total_bet_exceeds_balance() -> None:
    slot_machine = load_slot_machine()
    losing_slots = [
        ["A", "B", "C"],
        ["D", "C", "B"],
        ["A", "D", "C"],
    ]

    with (
        patch.object(slot_machine, "get_number_of_lines", return_value=2),
        patch.object(slot_machine, "get_bet", side_effect=[60, 5]),
        patch.object(slot_machine, "get_slot_machine_spin", return_value=losing_slots),
    ):
        new_balance, output = call_with_inputs(slot_machine.run_spin, [], 100)

    assert new_balance == 90
    assert "You do not have enough to bet that amount." in output
    assert "Total bet is $10." in output
    assert "No winning lines this spin." in output


def test_main_quits_cleanly() -> None:
    slot_machine = load_slot_machine()

    with (
        patch.object(slot_machine, "deposit_money", return_value=100),
        patch.object(slot_machine, "run_spin") as run_spin,
    ):
        output = run_with_inputs(slot_machine.main, [" Q "])

    run_spin.assert_not_called()
    assert "Current balance is $100." in output
    assert "You left with $100." in output
