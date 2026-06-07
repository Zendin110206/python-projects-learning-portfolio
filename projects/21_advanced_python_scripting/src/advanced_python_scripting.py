import argparse
import json
import shutil
import subprocess
from pathlib import Path

GAME_MARKER_FILES = ("game.json", "main.py", "main.go")
DEFAULT_METADATA_NAME = "metadata.json"

HEADER_TEXT = "Advanced Python Scripting - Game Packager"
SOURCE_MISSING_MESSAGE = "Source folder does not exist."
NO_GAMES_MESSAGE = "No game folders found."
DRY_RUN_MESSAGE = "Dry run enabled. No files were copied."
COPY_FAILURE_MESSAGE_TEMPLATE = "Copy failed for {game_name}."
METADATA_FAILURE_MESSAGE = "Metadata write failed."
GO_MISSING_MESSAGE = "Go is not installed or not available on PATH."
DONE_MESSAGE = "Done."


def build_parser():
    parser = argparse.ArgumentParser(description="Package local game folders.")
    parser.add_argument("--source", required=True, help="Folder containing game folders.")
    parser.add_argument("--destination", required=True, help="Folder where games will be copied.")
    parser.add_argument(
        "--metadata-name",
        default=DEFAULT_METADATA_NAME,
        help="Metadata JSON filename.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview copy operations without writing files.",
    )
    parser.add_argument(
        "--compile-go",
        action="store_true",
        help="Run go build for copied games that contain main.go.",
    )

    return parser


def parse_args(argv=None):
    parser = build_parser()
    return parser.parse_args(argv)


def validate_source(source_path):
    return source_path.exists() and source_path.is_dir()


def is_game_directory(path):
    if not path.is_dir():
        return False

    return any((path / marker).is_file() for marker in GAME_MARKER_FILES)


def find_game_directories(source_path):
    game_dirs = [path for path in source_path.iterdir() if is_game_directory(path)]
    return sorted(game_dirs, key=lambda path: path.name.lower())


def build_destination_path(destination_root, game_dir):
    return destination_root / game_dir.name


def copy_game_directory(game_dir, destination_path):
    shutil.copytree(game_dir, destination_path, dirs_exist_ok=True)
    return destination_path


def build_game_metadata(game_dir, destination_path):
    return {
        "name": game_dir.name,
        "source_path": str(game_dir),
        "destination_path": str(destination_path),
        "has_python": (game_dir / "main.py").is_file(),
        "has_go": (game_dir / "main.go").is_file(),
        "has_metadata": (game_dir / "game.json").is_file(),
    }


def write_metadata(destination_root, metadata_name, metadata):
    destination_root.mkdir(parents=True, exist_ok=True)
    metadata_path = destination_root / metadata_name
    metadata_text = json.dumps(metadata, indent=2)
    metadata_path.write_text(f"{metadata_text}\n", encoding="utf-8")

    return metadata_path


def run_go_build(game_dir):
    if not (game_dir / "main.go").is_file():
        return "skipped"

    try:
        subprocess.run(
            ["go", "build"],
            cwd=game_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"Go build completed: {game_dir.name}")
        return "success"

    except FileNotFoundError:
        print(GO_MISSING_MESSAGE)
        return "missing_go"

    except subprocess.CalledProcessError:
        print(f"Go build failed: {game_dir.name}")
        return "failed"


def process_games(source_path, destination_path, metadata_name, dry_run, compile_go):
    print(HEADER_TEXT)

    if not validate_source(source_path):
        print(SOURCE_MISSING_MESSAGE)
        return 1

    game_dirs = find_game_directories(source_path)

    if not game_dirs:
        print(NO_GAMES_MESSAGE)
        return 1

    print(f"Found {len(game_dirs)} game folder(s).")

    if dry_run:
        print(DRY_RUN_MESSAGE)
        for game_dir in game_dirs:
            copied_destination = build_destination_path(destination_path, game_dir)
            print(f"Would copy: {game_dir} -> {copied_destination}")

        print(DONE_MESSAGE)
        return 0

    destination_path.mkdir(parents=True, exist_ok=True)
    copied_games = []
    has_failure = False

    for game_dir in game_dirs:
        copied_destination = build_destination_path(destination_path, game_dir)

        try:
            copy_game_directory(game_dir, copied_destination)
            print(f"Copied: {game_dir.name}")

        except OSError:
            print(COPY_FAILURE_MESSAGE_TEMPLATE.format(game_name=game_dir.name))
            has_failure = True
            continue

        if compile_go:
            build_status = run_go_build(copied_destination)
            if build_status in ("missing_go", "failed"):
                has_failure = True

        copied_games.append(build_game_metadata(game_dir, copied_destination))

    metadata = {
        "source": str(source_path),
        "destination": str(destination_path),
        "games": copied_games,
    }

    try:
        metadata_path = write_metadata(destination_path, metadata_name, metadata)
        print(f"Metadata written: {metadata_path}")

    except (OSError, TypeError, ValueError):
        print(METADATA_FAILURE_MESSAGE)
        print(DONE_MESSAGE)
        return 1

    print(DONE_MESSAGE)

    if has_failure:
        return 1

    return 0


def main(argv=None):
    args = parse_args(argv)
    source_path = Path(args.source)
    destination_path = Path(args.destination)

    return process_games(
        source_path=source_path,
        destination_path=destination_path,
        metadata_name=args.metadata_name,
        dry_run=args.dry_run,
        compile_go=args.compile_go,
    )


if __name__ == "__main__":
    raise SystemExit(main())
