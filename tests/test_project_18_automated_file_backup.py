import importlib.util
import io
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "projects"
    / "18_automated_file_backup"
    / "src"
    / "automated_file_backup.py"
)


def load_automated_file_backup() -> ModuleType:
    spec = importlib.util.spec_from_file_location("automated_backup_under_test", SCRIPT)
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


def test_module_import_does_not_prompt_copy_or_schedule() -> None:
    with (
        patch("builtins.input") as input_mock,
        patch("shutil.copytree") as copytree,
        patch("schedule.every") as every,
    ):
        load_automated_file_backup()

    input_mock.assert_not_called()
    copytree.assert_not_called()
    every.assert_not_called()


def test_parse_folder_path_strips_input_and_rejects_empty_text() -> None:
    automated_backup = load_automated_file_backup()

    assert automated_backup.parse_folder_path("  D:\\Data  ") == Path("D:\\Data")
    assert automated_backup.parse_folder_path("   ") is None


def test_validate_source_folder_requires_existing_folder(tmp_path: Path) -> None:
    automated_backup = load_automated_file_backup()
    source_file = tmp_path / "notes.txt"
    missing_folder = tmp_path / "missing"
    source_file.write_text("hello", encoding="utf-8")

    assert automated_backup.validate_source_folder(tmp_path) is True
    assert automated_backup.validate_source_folder(source_file) is False
    assert automated_backup.validate_source_folder(missing_folder) is False
    assert automated_backup.validate_source_folder(None) is False


def test_validate_backup_folder_rejects_none_only(tmp_path: Path) -> None:
    automated_backup = load_automated_file_backup()

    assert automated_backup.validate_backup_folder(tmp_path / "backups") is True
    assert automated_backup.validate_backup_folder(None) is False


def test_folders_are_same_compares_resolved_paths(tmp_path: Path) -> None:
    automated_backup = load_automated_file_backup()
    source = tmp_path / "source"
    backups = tmp_path / "backups"
    source.mkdir()

    assert automated_backup.folders_are_same(source, source) is True
    assert automated_backup.folders_are_same(source, backups) is False


def test_create_backup_path_uses_timestamped_folder_name(tmp_path: Path) -> None:
    automated_backup = load_automated_file_backup()
    fixed_now = datetime(2026, 6, 7, 10, 30, 0)

    backup_path = automated_backup.create_backup_path(tmp_path, now=fixed_now)

    assert backup_path == tmp_path / "backup_2026-06-07_10-30-00"


def test_copy_folder_copies_source_tree(tmp_path: Path) -> None:
    automated_backup = load_automated_file_backup()
    source = tmp_path / "source"
    nested = source / "nested"
    backup_path = tmp_path / "backups" / "backup_2026-06-07_10-30-00"
    nested.mkdir(parents=True)
    (source / "notes.txt").write_text("hello", encoding="utf-8")
    (nested / "todo.txt").write_text("backup", encoding="utf-8")

    result = automated_backup.copy_folder(source, backup_path)

    assert result == backup_path
    assert (backup_path / "notes.txt").read_text(encoding="utf-8") == "hello"
    assert (backup_path / "nested" / "todo.txt").read_text(encoding="utf-8") == "backup"


def test_run_backup_job_creates_backup_and_prints_path(tmp_path: Path) -> None:
    automated_backup = load_automated_file_backup()
    source = tmp_path / "source"
    backup_root = tmp_path / "backups"
    backup_path = backup_root / "backup_fixed"
    source.mkdir()
    (source / "notes.txt").write_text("hello", encoding="utf-8")
    output = io.StringIO()

    with (
        patch.object(automated_backup, "create_backup_path", return_value=backup_path),
        redirect_stdout(output),
    ):
        result = automated_backup.run_backup_job(source, backup_root)

    assert result == backup_path
    assert backup_root.is_dir()
    assert (backup_path / "notes.txt").read_text(encoding="utf-8") == "hello"
    assert output.getvalue() == f"Backup created: {backup_path}\n"


def test_run_backup_job_handles_copy_failure(tmp_path: Path) -> None:
    automated_backup = load_automated_file_backup()
    source = tmp_path / "source"
    backup_root = tmp_path / "backups"
    source.mkdir()
    output = io.StringIO()

    with (
        patch.object(automated_backup, "copy_folder", side_effect=OSError("copy failed")),
        redirect_stdout(output),
    ):
        result = automated_backup.run_backup_job(source, backup_root)

    assert result is None
    assert output.getvalue() == f"{automated_backup.BACKUP_ERROR_MESSAGE}\n"


def test_is_valid_backup_time_accepts_hh_mm_only() -> None:
    automated_backup = load_automated_file_backup()

    assert automated_backup.is_valid_backup_time("07:30") is True
    assert automated_backup.is_valid_backup_time("18:45") is True
    assert automated_backup.is_valid_backup_time("23:59") is True
    assert automated_backup.is_valid_backup_time("7:30") is False
    assert automated_backup.is_valid_backup_time("24:00") is False
    assert automated_backup.is_valid_backup_time("18.30") is False
    assert automated_backup.is_valid_backup_time("abc") is False


def test_start_scheduler_registers_daily_job_and_stops_cleanly(tmp_path: Path) -> None:
    automated_backup = load_automated_file_backup()
    source = tmp_path / "source"
    backup_root = tmp_path / "backups"
    source.mkdir()
    output = io.StringIO()
    day = Mock()
    job = Mock()
    automated_backup.schedule.clear()

    with (
        patch.object(automated_backup.schedule, "every", return_value=day) as every,
        patch.object(automated_backup.schedule, "run_pending") as run_pending,
        patch.object(automated_backup.time, "sleep", side_effect=KeyboardInterrupt),
        redirect_stdout(output),
    ):
        day.day = job
        automated_backup.start_scheduler(source, backup_root, "18:30")

    every.assert_called_once_with()
    job.at.assert_called_once_with("18:30")
    job.at.return_value.do.assert_called_once_with(
        automated_backup.run_backup_job,
        source,
        backup_root,
    )
    run_pending.assert_called_once_with()
    assert "Scheduled daily backup at 18:30. Press Ctrl+C to stop." in output.getvalue()
    assert automated_backup.SCHEDULER_STOPPED_MESSAGE in output.getvalue()


def test_main_handles_invalid_inputs_and_run_now(tmp_path: Path) -> None:
    automated_backup = load_automated_file_backup()
    source = tmp_path / "source"
    backup_root = tmp_path / "backups"
    source.mkdir()

    _, missing_source_output = call_with_inputs(
        automated_backup.main,
        [str(tmp_path / "missing"), str(backup_root), ""],
    )
    _, empty_backup_output = call_with_inputs(
        automated_backup.main,
        [str(source), "   ", ""],
    )
    _, same_folder_output = call_with_inputs(
        automated_backup.main,
        [str(source), str(source), ""],
    )
    _, invalid_time_output = call_with_inputs(
        automated_backup.main,
        [str(source), str(backup_root), "7:30"],
    )

    with patch.object(automated_backup, "run_backup_job") as run_backup_job:
        _, run_now_output = call_with_inputs(
            automated_backup.main,
            [str(source), str(backup_root), ""],
        )

    assert automated_backup.SOURCE_MISSING_MESSAGE in missing_source_output
    assert automated_backup.BACKUP_EMPTY_MESSAGE in empty_backup_output
    assert automated_backup.SAME_FOLDER_MESSAGE in same_folder_output
    assert automated_backup.INVALID_TIME_MESSAGE in invalid_time_output
    run_backup_job.assert_called_once_with(source, backup_root)
    assert run_now_output.endswith("Enter backup time (HH:MM) or press Enter to run now: ")


def test_main_starts_scheduler_for_valid_time(tmp_path: Path) -> None:
    automated_backup = load_automated_file_backup()
    source = tmp_path / "source"
    backup_root = tmp_path / "backups"
    source.mkdir()

    with patch.object(automated_backup, "start_scheduler") as start_scheduler:
        call_with_inputs(
            automated_backup.main,
            [str(source), str(backup_root), "18:30"],
        )

    start_scheduler.assert_called_once_with(source, backup_root, "18:30")
