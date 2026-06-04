import csv
import importlib.util
import io
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "15_expense_tracker" / "src" / "expense_tracker.py"


def load_expense_tracker() -> ModuleType:
    spec = importlib.util.spec_from_file_location("expense_tracker_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def use_temp_data_file(expense_tracker: ModuleType, tmp_path: Path) -> Path:
    data_dir = tmp_path / "data"
    data_file = data_dir / "expenses.csv"

    expense_tracker.DATA_DIR = data_dir
    expense_tracker.DATA_FILE = data_file

    return data_file


def call_with_inputs(function, player_inputs: list[str], *args):
    inputs = iter(player_inputs)
    output = io.StringIO()

    def fake_input(prompt: str = "") -> str:
        print(prompt, end="")
        return next(inputs)

    with patch("builtins.input", fake_input), redirect_stdout(output):
        result = function(*args)

    return result, output.getvalue()


def capture_main_with_inputs(expense_tracker: ModuleType, player_inputs: list[str]) -> str:
    _, output = call_with_inputs(expense_tracker.main, player_inputs)

    return output


def test_module_import_does_not_run_main() -> None:
    with patch("builtins.input") as input_mock:
        load_expense_tracker()

    input_mock.assert_not_called()


def test_ensure_data_file_creates_header(tmp_path: Path) -> None:
    expense_tracker = load_expense_tracker()
    data_file = use_temp_data_file(expense_tracker, tmp_path)

    expense_tracker.ensure_data_file()

    assert data_file.read_text(encoding="utf-8").splitlines() == [
        "date,category,description,amount",
    ]


def test_parse_date_accepts_valid_yyyy_mm_dd_only() -> None:
    expense_tracker = load_expense_tracker()

    assert expense_tracker.parse_date("2026-06-05") == "2026-06-05"
    assert expense_tracker.parse_date("05-06-2026") is None
    assert expense_tracker.parse_date("2026-13-01") is None
    assert expense_tracker.parse_date("2026-02-30") is None


def test_parse_amount_accepts_positive_finite_numbers_only() -> None:
    expense_tracker = load_expense_tracker()

    assert expense_tracker.parse_amount("25000") == Decimal("25000")
    assert expense_tracker.parse_amount("12500.50") == Decimal("12500.50")
    assert expense_tracker.parse_amount("0") is None
    assert expense_tracker.parse_amount("-10") is None
    assert expense_tracker.parse_amount("abc") is None
    assert expense_tracker.parse_amount("Infinity") is None


def test_save_and_read_expenses_round_trip(tmp_path: Path) -> None:
    expense_tracker = load_expense_tracker()
    use_temp_data_file(expense_tracker, tmp_path)
    expense_tracker.ensure_data_file()

    expense_tracker.save_expense(
        {
            "date": "2026-06-05",
            "category": "Food",
            "description": "Lunch",
            "amount": "25000",
        }
    )

    assert expense_tracker.read_expenses() == [
        {
            "date": "2026-06-05",
            "category": "Food",
            "description": "Lunch",
            "amount": "25000",
        }
    ]


def test_read_expenses_returns_empty_list_when_file_is_missing(tmp_path: Path) -> None:
    expense_tracker = load_expense_tracker()
    use_temp_data_file(expense_tracker, tmp_path)

    assert expense_tracker.read_expenses() == []


def test_format_expenses_handles_empty_and_existing_records() -> None:
    expense_tracker = load_expense_tracker()

    assert expense_tracker.format_expenses([]) == (
        "Expenses\n"
        "No expenses recorded yet."
    )
    assert expense_tracker.format_expenses(
        [
            {
                "date": "2026-06-05",
                "category": "Food",
                "description": "Lunch",
                "amount": "25000",
            }
        ]
    ) == "Expenses\n2026-06-05 | Food | Lunch | 25000.00"


def test_calculate_and_format_totals_by_category() -> None:
    expense_tracker = load_expense_tracker()
    expenses = [
        {"category": "Food", "amount": "25000"},
        {"category": "Transport", "amount": "12000"},
        {"category": "Food", "amount": "15000"},
    ]

    totals = expense_tracker.calculate_totals(expenses)

    assert totals == {
        "Food": Decimal("40000"),
        "Transport": Decimal("12000"),
    }
    assert expense_tracker.format_totals(totals) == (
        "Totals by Category\n"
        "Food - 40000.00\n"
        "Transport - 12000.00"
    )
    assert expense_tracker.format_totals({}) == (
        "Totals by Category\n"
        "No expenses recorded yet."
    )


def test_prompt_for_expense_retries_until_valid_values() -> None:
    expense_tracker = load_expense_tracker()

    expense, output = call_with_inputs(
        expense_tracker.prompt_for_expense,
        [
            "abc",
            "2026-06-05",
            "",
            "food",
            "",
            "lunch",
            "-5",
            "25000",
        ],
    )

    assert expense == {
        "date": "2026-06-05",
        "category": "Food",
        "description": "Lunch",
        "amount": "25000",
    }
    assert "Invalid date. Please use YYYY-MM-DD." in output
    assert "Category cannot be empty." in output
    assert "Description cannot be empty." in output
    assert "Amount must be a positive number." in output


def test_main_handles_invalid_input_then_exit(tmp_path: Path) -> None:
    expense_tracker = load_expense_tracker()
    use_temp_data_file(expense_tracker, tmp_path)

    output = capture_main_with_inputs(expense_tracker, ["abc", "4"])

    assert "Please choose 1, 2, 3, or 4." in output
    assert output.rstrip().endswith("Goodbye.")


def test_main_can_add_list_and_summarize_expense(tmp_path: Path) -> None:
    expense_tracker = load_expense_tracker()
    data_file = use_temp_data_file(expense_tracker, tmp_path)

    output = capture_main_with_inputs(
        expense_tracker,
        [
            "1",
            "2026-06-05",
            "food",
            "lunch",
            "25000",
            "2",
            "3",
            "4",
        ],
    )

    assert "Expense saved." in output
    assert "2026-06-05 | Food | Lunch | 25000.00" in output
    assert "Food - 25000.00" in output
    assert output.rstrip().endswith("Goodbye.")

    with data_file.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert rows == [
        {
            "date": "2026-06-05",
            "category": "Food",
            "description": "Lunch",
            "amount": "25000",
        }
    ]
