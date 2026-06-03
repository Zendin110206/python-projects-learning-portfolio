import importlib.util
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / "projects" / "11_wpm_typing_test"
SCRIPT = PROJECT_DIR / "src" / "wpm_typing_test.py"
TEXT_FILE = PROJECT_DIR / "text.txt"


def load_wpm_typing_test() -> ModuleType:
    spec = importlib.util.spec_from_file_location("wpm_typing_test_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


class FakeScreen:
    def __init__(self, keys: list[str] | None = None) -> None:
        self.keys = keys or []
        self.clear_count = 0
        self.refresh_count = 0
        self.nodelay_values = []
        self.added_strings = []

    def clear(self) -> None:
        self.clear_count += 1

    def addstr(self, *args) -> None:
        self.added_strings.append(args)

    def refresh(self) -> None:
        self.refresh_count += 1

    def getkey(self) -> str:
        if not self.keys:
            raise RuntimeError("No fake keys remaining.")

        return self.keys.pop(0)

    def nodelay(self, value: bool) -> None:
        self.nodelay_values.append(value)


def test_module_import_does_not_start_curses_wrapper() -> None:
    with patch("curses.wrapper") as wrapper:
        load_wpm_typing_test()

    wrapper.assert_not_called()


def test_load_prompts_reads_non_empty_lines() -> None:
    wpm_typing_test = load_wpm_typing_test()

    prompts = wpm_typing_test.load_prompts()

    assert prompts == [
        "Typing helps build accuracy before speed.",
        "Python projects are easier when practiced step by step.",
        "Clean code is readable code.",
        "Terminal apps can still feel interactive.",
    ]


def test_choose_prompt_uses_random_choice() -> None:
    wpm_typing_test = load_wpm_typing_test()

    with patch.object(wpm_typing_test.random, "choice", return_value="Clean code."):
        prompt = wpm_typing_test.choose_prompt(["Clean code.", "Other text."])

    assert prompt == "Clean code."


def test_calculate_wpm_uses_minimum_elapsed_second() -> None:
    wpm_typing_test = load_wpm_typing_test()

    assert wpm_typing_test.calculate_wpm(character_count=10, elapsed_seconds=0) == 120
    assert wpm_typing_test.calculate_wpm(character_count=25, elapsed_seconds=30) == 10


def test_is_escape_key_detects_escape_character() -> None:
    wpm_typing_test = load_wpm_typing_test()

    assert wpm_typing_test.is_escape_key("\x1b") is True
    assert wpm_typing_test.is_escape_key("a") is False
    assert wpm_typing_test.is_escape_key("KEY_BACKSPACE") is False


def test_start_screen_displays_welcome_text_and_waits_for_key() -> None:
    wpm_typing_test = load_wpm_typing_test()
    screen = FakeScreen(keys=["x"])

    wpm_typing_test.start_screen(screen)

    assert screen.clear_count == 1
    assert (0, 0, "Welcome to the WPM Typing Test!") in screen.added_strings
    assert (1, 0, "Press any key to begin.") in screen.added_strings
    assert screen.refresh_count == 1
    assert screen.keys == []


def test_display_text_marks_correct_and_incorrect_characters() -> None:
    wpm_typing_test = load_wpm_typing_test()
    screen = FakeScreen()

    with patch.object(wpm_typing_test.curses, "color_pair", side_effect=lambda value: value):
        wpm_typing_test.display_text(
            screen,
            target_text="ab",
            current_text=["a", "x"],
            wpm=42,
        )

    assert (0, 0, "ab") in screen.added_strings
    assert (1, 0, "WPM: 42") in screen.added_strings
    assert (2, 0, "Press Esc to exit.") in screen.added_strings
    assert (0, 0, "a", wpm_typing_test.GREEN_PAIR) in screen.added_strings
    assert (0, 1, "x", wpm_typing_test.RED_PAIR) in screen.added_strings


def test_handle_key_supports_backspace_and_regular_characters() -> None:
    wpm_typing_test = load_wpm_typing_test()
    current_text = ["a", "b"]

    wpm_typing_test.handle_key(current_text, "KEY_BACKSPACE", "abcd")
    assert current_text == ["a"]

    wpm_typing_test.handle_key(current_text, "c", "abcd")
    assert current_text == ["a", "c"]

    wpm_typing_test.handle_key(current_text, "KEY_LEFT", "abcd")
    assert current_text == ["a", "c"]


def test_run_typing_round_completes_text_and_allows_continue() -> None:
    wpm_typing_test = load_wpm_typing_test()
    screen = FakeScreen(keys=["a", "b", "x"])

    with (
        patch.object(wpm_typing_test.time, "time", side_effect=[0, 1, 2, 3]),
        patch.object(wpm_typing_test, "display_text") as display_text,
    ):
        wants_to_quit = wpm_typing_test.run_typing_round(screen, "ab")

    assert wants_to_quit is None
    assert screen.nodelay_values == [True, False]
    assert (4, 0, "You completed the text! Press any key to continue.") in (
        screen.added_strings
    )
    assert display_text.call_count == 3


def test_run_typing_round_returns_true_when_escape_is_pressed() -> None:
    wpm_typing_test = load_wpm_typing_test()
    screen = FakeScreen(keys=["\x1b"])

    with (
        patch.object(wpm_typing_test.time, "time", side_effect=[0, 1]),
        patch.object(wpm_typing_test, "display_text"),
    ):
        wants_to_quit = wpm_typing_test.run_typing_round(screen, "abc")

    assert wants_to_quit is True
    assert screen.nodelay_values == [True, False]


def test_main_initializes_colors_and_runs_until_user_quits() -> None:
    wpm_typing_test = load_wpm_typing_test()
    screen = FakeScreen()

    with (
        patch.object(wpm_typing_test, "initialize_colors") as initialize_colors,
        patch.object(wpm_typing_test, "start_screen") as start_screen,
        patch.object(wpm_typing_test, "load_prompts", return_value=["abc"]),
        patch.object(wpm_typing_test, "choose_prompt", return_value="abc"),
        patch.object(wpm_typing_test, "run_typing_round", side_effect=[False, True]),
    ):
        wpm_typing_test.main(screen)

    initialize_colors.assert_called_once_with()
    start_screen.assert_called_once_with(screen)


def test_text_file_exists_with_expected_prompts() -> None:
    assert TEXT_FILE.read_text(encoding="utf-8").splitlines() == [
        "Typing helps build accuracy before speed.",
        "Python projects are easier when practiced step by step.",
        "Clean code is readable code.",
        "Terminal apps can still feel interactive.",
    ]
