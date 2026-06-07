import importlib.util
import io
import json
import subprocess
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "projects"
    / "21_advanced_python_scripting"
    / "src"
    / "advanced_python_scripting.py"
)


def load_advanced_python_scripting() -> ModuleType:
    spec = importlib.util.spec_from_file_location("advanced_scripting_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def capture_output(function, *args, **kwargs):
    output = io.StringIO()

    with redirect_stdout(output):
        result = function(*args, **kwargs)

    return result, output.getvalue()


def make_game_folder(root: Path, name: str, marker: str, content: str = "") -> Path:
    game_dir = root / name
    game_dir.mkdir(parents=True)
    (game_dir / marker).write_text(content, encoding="utf-8")

    return game_dir


def test_module_import_does_not_run_cli() -> None:
    with patch("argparse.ArgumentParser.parse_args") as parse_args:
        load_advanced_python_scripting()

    parse_args.assert_not_called()


def test_parse_args_reads_required_and_optional_arguments() -> None:
    script = load_advanced_python_scripting()

    args = script.parse_args(
        [
            "--source",
            "source",
            "--destination",
            "output",
            "--metadata-name",
            "games.json",
            "--dry-run",
            "--compile-go",
        ]
    )

    assert args.source == "source"
    assert args.destination == "output"
    assert args.metadata_name == "games.json"
    assert args.dry_run is True
    assert args.compile_go is True


def test_validate_source_requires_existing_folder(tmp_path: Path) -> None:
    script = load_advanced_python_scripting()
    file_path = tmp_path / "notes.txt"
    missing_path = tmp_path / "missing"
    file_path.write_text("notes", encoding="utf-8")

    assert script.validate_source(tmp_path) is True
    assert script.validate_source(file_path) is False
    assert script.validate_source(missing_path) is False


def test_game_directory_detection_accepts_marker_files(tmp_path: Path) -> None:
    script = load_advanced_python_scripting()
    python_game = make_game_folder(tmp_path, "snake", "main.py")
    go_game = make_game_folder(tmp_path, "space", "main.go")
    metadata_game = make_game_folder(tmp_path, "pong", "game.json", "{}")
    invalid_folder = tmp_path / "notes"
    regular_file = tmp_path / "readme.txt"
    invalid_folder.mkdir()
    regular_file.write_text("hello", encoding="utf-8")

    assert script.is_game_directory(python_game) is True
    assert script.is_game_directory(go_game) is True
    assert script.is_game_directory(metadata_game) is True
    assert script.is_game_directory(invalid_folder) is False
    assert script.is_game_directory(regular_file) is False


def test_find_game_directories_returns_sorted_immediate_game_folders(tmp_path: Path) -> None:
    script = load_advanced_python_scripting()
    make_game_folder(tmp_path, "snake", "main.py")
    make_game_folder(tmp_path, "pong", "game.json", "{}")
    make_game_folder(tmp_path, "arcade", "main.go")
    (tmp_path / "notes").mkdir()

    game_dirs = script.find_game_directories(tmp_path)

    assert [path.name for path in game_dirs] == ["arcade", "pong", "snake"]


def test_dry_run_prints_copy_plan_without_writing_files(tmp_path: Path) -> None:
    script = load_advanced_python_scripting()
    source = tmp_path / "source"
    destination = tmp_path / "output"
    make_game_folder(source, "snake", "main.py")
    make_game_folder(source, "pong", "game.json", "{}")

    result, output = capture_output(
        script.process_games,
        source_path=source,
        destination_path=destination,
        metadata_name="metadata.json",
        dry_run=True,
        compile_go=False,
    )

    assert result == 0
    assert script.HEADER_TEXT in output
    assert "Found 2 game folder(s)." in output
    assert script.DRY_RUN_MESSAGE in output
    assert f"Would copy: {source / 'pong'} -> {destination / 'pong'}" in output
    assert f"Would copy: {source / 'snake'} -> {destination / 'snake'}" in output
    assert output.rstrip().endswith(script.DONE_MESSAGE)
    assert not destination.exists()


def test_real_copy_writes_games_and_metadata(tmp_path: Path) -> None:
    script = load_advanced_python_scripting()
    source = tmp_path / "source"
    destination = tmp_path / "output"
    snake = make_game_folder(source, "snake", "main.py", "print('snake')")
    pong = make_game_folder(source, "pong", "game.json", "{}")

    result, output = capture_output(
        script.process_games,
        source_path=source,
        destination_path=destination,
        metadata_name="metadata.json",
        dry_run=False,
        compile_go=False,
    )

    metadata = json.loads((destination / "metadata.json").read_text(encoding="utf-8"))

    assert result == 0
    assert (destination / "snake" / "main.py").read_text(encoding="utf-8") == (
        "print('snake')"
    )
    assert (destination / "pong" / "game.json").read_text(encoding="utf-8") == "{}"
    assert metadata == {
        "source": str(source),
        "destination": str(destination),
        "games": [
            {
                "name": "pong",
                "source_path": str(pong),
                "destination_path": str(destination / "pong"),
                "has_python": False,
                "has_go": False,
                "has_metadata": True,
            },
            {
                "name": "snake",
                "source_path": str(snake),
                "destination_path": str(destination / "snake"),
                "has_python": True,
                "has_go": False,
                "has_metadata": False,
            },
        ],
    }
    assert "Copied: pong" in output
    assert "Copied: snake" in output
    assert f"Metadata written: {destination / 'metadata.json'}" in output


def test_process_games_reports_missing_source_and_empty_source(tmp_path: Path) -> None:
    script = load_advanced_python_scripting()
    empty_source = tmp_path / "empty"
    empty_source.mkdir()

    missing_result, missing_output = capture_output(
        script.process_games,
        source_path=tmp_path / "missing",
        destination_path=tmp_path / "output",
        metadata_name="metadata.json",
        dry_run=False,
        compile_go=False,
    )
    empty_result, empty_output = capture_output(
        script.process_games,
        source_path=empty_source,
        destination_path=tmp_path / "output",
        metadata_name="metadata.json",
        dry_run=False,
        compile_go=False,
    )

    assert missing_result == 1
    assert script.SOURCE_MISSING_MESSAGE in missing_output
    assert empty_result == 1
    assert script.NO_GAMES_MESSAGE in empty_output


def test_copy_failure_is_reported_and_returns_failure(tmp_path: Path) -> None:
    script = load_advanced_python_scripting()
    source = tmp_path / "source"
    destination = tmp_path / "output"
    make_game_folder(source, "snake", "main.py")

    with patch.object(script, "copy_game_directory", side_effect=OSError("copy failed")):
        result, output = capture_output(
            script.process_games,
            source_path=source,
            destination_path=destination,
            metadata_name="metadata.json",
            dry_run=False,
            compile_go=False,
        )

    assert result == 1
    assert "Copy failed for snake." in output
    assert script.DONE_MESSAGE in output


def test_metadata_failure_is_reported_and_returns_failure(tmp_path: Path) -> None:
    script = load_advanced_python_scripting()
    source = tmp_path / "source"
    destination = tmp_path / "output"
    make_game_folder(source, "snake", "main.py")

    with patch.object(script, "write_metadata", side_effect=OSError("write failed")):
        result, output = capture_output(
            script.process_games,
            source_path=source,
            destination_path=destination,
            metadata_name="metadata.json",
            dry_run=False,
            compile_go=False,
        )

    assert result == 1
    assert script.METADATA_FAILURE_MESSAGE in output
    assert output.rstrip().endswith(script.DONE_MESSAGE)


def test_run_go_build_skips_non_go_games(tmp_path: Path) -> None:
    script = load_advanced_python_scripting()
    game_dir = make_game_folder(tmp_path, "snake", "main.py")

    with patch.object(script.subprocess, "run") as run:
        result, output = capture_output(script.run_go_build, game_dir)

    assert result == "skipped"
    assert output == ""
    run.assert_not_called()


def test_run_go_build_success(tmp_path: Path) -> None:
    script = load_advanced_python_scripting()
    game_dir = make_game_folder(tmp_path, "space", "main.go")

    with patch.object(script.subprocess, "run", return_value=Mock()) as run:
        result, output = capture_output(script.run_go_build, game_dir)

    assert result == "success"
    assert "Go build completed: space" in output
    run.assert_called_once_with(
        ["go", "build"],
        cwd=game_dir,
        check=True,
        capture_output=True,
        text=True,
    )


def test_run_go_build_handles_missing_go_and_failed_build(tmp_path: Path) -> None:
    script = load_advanced_python_scripting()
    game_dir = make_game_folder(tmp_path, "space", "main.go")

    with patch.object(script.subprocess, "run", side_effect=FileNotFoundError):
        missing_result, missing_output = capture_output(script.run_go_build, game_dir)

    with patch.object(
        script.subprocess,
        "run",
        side_effect=subprocess.CalledProcessError(1, ["go", "build"]),
    ):
        failed_result, failed_output = capture_output(script.run_go_build, game_dir)

    assert missing_result == "missing_go"
    assert script.GO_MISSING_MESSAGE in missing_output
    assert failed_result == "failed"
    assert "Go build failed: space" in failed_output
