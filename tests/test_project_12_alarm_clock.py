import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "12_alarm_clock" / "src" / "alarm_clock.py"


def load_alarm_clock() -> ModuleType:
    spec = importlib.util.spec_from_file_location("alarm_clock_under_test", SCRIPT)
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


def capture_output(function, *args) -> str:
    output = io.StringIO()

    with redirect_stdout(output):
        function(*args)

    return output.getvalue()


def test_parse_duration_accepts_valid_duration() -> None:
    alarm_clock = load_alarm_clock()

    assert alarm_clock.parse_duration("01:02:03") == 3723
    assert alarm_clock.parse_duration(" 00:00:05 ") == 5


def test_parse_duration_rejects_invalid_format() -> None:
    alarm_clock = load_alarm_clock()

    output = capture_output(alarm_clock.parse_duration, "abc")

    assert "Invalid format. Please use HH:MM:SS." in output
    assert alarm_clock.parse_duration("00:00") is None


def test_parse_duration_rejects_invalid_minute_or_second_range() -> None:
    alarm_clock = load_alarm_clock()

    output = capture_output(alarm_clock.parse_duration, "00:60:00")

    assert "Minutes and seconds must be between 0 and 59." in output
    assert alarm_clock.parse_duration("00:00:60") is None


def test_parse_duration_rejects_zero_duration() -> None:
    alarm_clock = load_alarm_clock()

    output = capture_output(alarm_clock.parse_duration, "00:00:00")

    assert "Duration must be greater than 0 seconds." in output
    assert alarm_clock.parse_duration("00:00:00") is None


def test_format_duration_uses_hh_mm_ss() -> None:
    alarm_clock = load_alarm_clock()

    assert alarm_clock.format_duration(0) == "00:00:00"
    assert alarm_clock.format_duration(5) == "00:00:05"
    assert alarm_clock.format_duration(90) == "00:01:30"
    assert alarm_clock.format_duration(3723) == "01:02:03"


def test_get_alarm_duration_retries_until_valid_input() -> None:
    alarm_clock = load_alarm_clock()

    total_seconds, output = call_with_inputs(
        alarm_clock.get_alarm_duration,
        ["abc", "00:60:00", "00:00:00", "00:00:03"],
    )

    assert total_seconds == 3
    assert "Invalid format. Please use HH:MM:SS." in output
    assert "Minutes and seconds must be between 0 and 59." in output
    assert "Duration must be greater than 0 seconds." in output


def test_run_countdown_prints_remaining_time_and_final_message() -> None:
    alarm_clock = load_alarm_clock()

    with patch.object(alarm_clock.time, "sleep") as sleep:
        output = capture_output(alarm_clock.run_countdown, 3)

    assert output == (
        "Time remaining: 00:00:03\n"
        "Time remaining: 00:00:02\n"
        "Time remaining: 00:00:01\n"
        "Wake up! Alarm finished.\n"
    )
    assert sleep.call_count == 3


def test_main_prints_alarm_set_and_runs_countdown() -> None:
    alarm_clock = load_alarm_clock()

    with (
        patch.object(alarm_clock, "get_alarm_duration", return_value=5),
        patch.object(alarm_clock, "run_countdown") as run_countdown,
    ):
        output = capture_output(alarm_clock.main)

    assert output == "Alarm set for 00:00:05.\n"
    run_countdown.assert_called_once_with(5)
