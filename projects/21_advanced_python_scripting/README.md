# Project 21 - Advanced Python Scripting

Status: In progress.

This project is a command-line automation script for packaging local game folders. It is intended for practicing command-line arguments, directory scanning, folder copying, JSON metadata generation, dry-run workflows, and optional subprocess execution.

## Goal

Build a terminal script that:

- accepts source and destination folders from command-line arguments,
- finds valid game folders inside the source folder,
- copies each game folder into the destination folder,
- writes a metadata JSON file,
- supports a dry-run mode,
- optionally runs an external build command for copied Go projects,
- handles missing folders, empty results, copy errors, JSON errors, and subprocess errors clearly.

## Learning Focus

- building command-line interfaces with `argparse`,
- working with `pathlib` paths,
- scanning folders safely,
- copying directory trees with `shutil.copytree`,
- writing structured JSON with `json`,
- using `subprocess.run` defensively,
- keeping CLI parsing, file operations, metadata, and terminal output separate.

## Planned Run Command

The exact command will be finalized after the implementation is added. The intended shape is:

```powershell
python projects/21_advanced_python_scripting/src/advanced_python_scripting.py --source SOURCE --destination DESTINATION
```

## Expected Terminal Behavior

A valid run should print a short header, show how many game folders were found, copy each game folder, write metadata, and finish with a clear success message.

Invalid source folders, empty results, copy failures, metadata failures, and optional subprocess failures should be handled with clear messages.

## Completion Checklist

- The script can be run from the terminal.
- CLI arguments are parsed with `argparse`.
- Source and destination folders are validated.
- Game folders are detected consistently.
- Dry-run mode does not copy files.
- Copied folders are written to the destination.
- Metadata JSON is generated.
- Optional subprocess behavior is isolated and testable.
- Core logic is covered by automated tests.

## Notes

- This project uses only the Python standard library.
- Local source and output folders should stay out of version control.
- Go compilation is optional and should not be required for the default run.
