import importlib.util
import io
import string
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "13_password_generator" / "src" / "password_generator.py"


def load_password_generator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("password_generator_under_test", SCRIPT)
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


def test_get_password_length_retries_until_valid_length() -> None:
    password_generator = load_password_generator()

    length, output = call_with_inputs(
        password_generator.get_password_length,
        ["abc", "7", "65", "12"],
    )

    assert length == 12
    assert "Please enter a number." in output
    assert output.count("Password length must be between 8 and 64.") == 2


def test_ask_yes_no_accepts_normalized_y_and_n() -> None:
    password_generator = load_password_generator()

    wants_uppercase, uppercase_output = call_with_inputs(
        password_generator.ask_yes_no,
        ["maybe", " Y "],
        "Include uppercase letters? (y/n): ",
    )
    wants_numbers, numbers_output = call_with_inputs(
        password_generator.ask_yes_no,
        [" n "],
        "Include numbers? (y/n): ",
    )

    assert wants_uppercase is True
    assert wants_numbers is False
    assert "Please enter y or n." in uppercase_output
    assert "Please enter y or n." not in numbers_output


def test_build_character_groups_always_includes_lowercase() -> None:
    password_generator = load_password_generator()

    required_groups, character_pool = password_generator.build_character_groups(
        include_uppercase=False,
        include_numbers=False,
        include_symbols=False,
    )

    assert required_groups == [string.ascii_lowercase]
    assert character_pool == string.ascii_lowercase


def test_build_character_groups_adds_selected_groups() -> None:
    password_generator = load_password_generator()

    required_groups, character_pool = password_generator.build_character_groups(
        include_uppercase=True,
        include_numbers=True,
        include_symbols=True,
    )

    assert required_groups == [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation,
    ]
    assert character_pool == (
        string.ascii_lowercase
        + string.ascii_uppercase
        + string.digits
        + string.punctuation
    )


def test_secure_shuffle_uses_secure_random_indexes() -> None:
    password_generator = load_password_generator()
    password_chars = ["a", "b", "c"]

    with patch.object(password_generator.secrets, "randbelow", side_effect=[0, 0]):
        password_generator.secure_shuffle(password_chars)

    assert password_chars == ["b", "c", "a"]


def test_generate_password_includes_each_selected_group() -> None:
    password_generator = load_password_generator()

    with (
        patch.object(password_generator.secrets, "choice", side_effect=list("aA7!bB8?")),
        patch.object(password_generator, "secure_shuffle"),
    ):
        password = password_generator.generate_password(
            length=8,
            include_uppercase=True,
            include_numbers=True,
            include_symbols=True,
        )

    assert password == "aA7!bB8?"
    assert any(char in string.ascii_lowercase for char in password)
    assert any(char in string.ascii_uppercase for char in password)
    assert any(char in string.digits for char in password)
    assert any(char in string.punctuation for char in password)


def test_generate_password_supports_lowercase_only() -> None:
    password_generator = load_password_generator()

    with (
        patch.object(password_generator.secrets, "choice", side_effect=list("abcdefgh")),
        patch.object(password_generator, "secure_shuffle"),
    ):
        password = password_generator.generate_password(
            length=8,
            include_uppercase=False,
            include_numbers=False,
            include_symbols=False,
        )

    assert password == "abcdefgh"
    assert password.islower()


def test_main_prints_generated_password() -> None:
    password_generator = load_password_generator()

    with (
        patch.object(password_generator, "get_password_length", return_value=12),
        patch.object(password_generator, "ask_yes_no", side_effect=[True, True, True]),
        patch.object(password_generator, "generate_password", return_value="aB7#xP2!mQ9z"),
    ):
        output = capture_output(password_generator.main)

    assert output == "Generated password: aB7#xP2!mQ9z\n"
