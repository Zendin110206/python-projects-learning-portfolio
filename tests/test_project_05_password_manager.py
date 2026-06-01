import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

from cryptography.fernet import Fernet

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "projects" / "05_password_manager" / "src" / "password_manager.py"


def load_password_manager(tmp_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("password_manager_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.project_dir = tmp_path
    module.data_dir = tmp_path / "data"
    module.key_file = module.data_dir / "key.key"
    module.passwords_file = module.data_dir / "passwords.txt"

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


def test_password_manager_creates_and_reuses_key(tmp_path: Path) -> None:
    password_manager = load_password_manager(tmp_path)

    password_manager.ensure_data_dir()
    first_key = password_manager.load_or_create_key()
    second_key = password_manager.load_or_create_key()

    assert password_manager.key_file.is_file()
    assert first_key == second_key


def test_password_manager_adds_encrypted_password_and_views_plaintext(
    tmp_path: Path,
) -> None:
    password_manager = load_password_manager(tmp_path)
    password_manager.ensure_data_dir()
    fernet = Fernet(password_manager.load_or_create_key())

    add_output = run_with_inputs(
        password_manager.add_password,
        ["email", "example-password"],
        fernet,
    )
    view_output = run_with_inputs(password_manager.view_passwords, [], fernet)
    saved_text = password_manager.passwords_file.read_text(encoding="utf-8")

    assert "Password saved." in add_output
    assert "Account: email | Password: example-password" in view_output
    assert "email|" in saved_text
    assert "example-password" not in saved_text


def test_password_manager_view_reports_empty_file(tmp_path: Path) -> None:
    password_manager = load_password_manager(tmp_path)
    password_manager.ensure_data_dir()
    password_manager.passwords_file.write_text("", encoding="utf-8")
    fernet = Fernet(password_manager.load_or_create_key())

    output = run_with_inputs(password_manager.view_passwords, [], fernet)

    assert "No passwords saved yet." in output


def test_password_manager_rejects_empty_account(tmp_path: Path) -> None:
    password_manager = load_password_manager(tmp_path)
    password_manager.ensure_data_dir()
    fernet = Fernet(password_manager.load_or_create_key())

    output = run_with_inputs(password_manager.add_password, ["", "unused"], fernet)

    assert "Account name cannot be empty." in output
    assert not password_manager.passwords_file.exists()


def test_password_manager_rejects_empty_password(tmp_path: Path) -> None:
    password_manager = load_password_manager(tmp_path)
    password_manager.ensure_data_dir()
    fernet = Fernet(password_manager.load_or_create_key())

    output = run_with_inputs(password_manager.add_password, ["email", ""], fernet)

    assert "Password cannot be empty." in output
    assert not password_manager.passwords_file.exists()


def test_password_manager_main_handles_invalid_mode_and_quit(tmp_path: Path) -> None:
    password_manager = load_password_manager(tmp_path)

    output = run_with_inputs(password_manager.main, ["delete", "q"])

    assert "Invalid mode. Please type add, view, or q." in output
    assert "Goodbye!" in output
