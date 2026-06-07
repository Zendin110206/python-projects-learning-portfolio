# Project 18 - Automated File Backup

Status: Completed.

This project is a scheduled folder backup utility. It is intended for practicing file-system automation, folder validation, timestamped backup naming, scheduled jobs, and clear terminal feedback for file operations.

## Goal

Build a terminal program that:

- asks for a source folder,
- asks for a destination backup folder,
- can run one backup immediately,
- can schedule a daily backup at a valid `HH:MM` time,
- copies the source folder into a timestamped backup folder,
- handles missing folders, invalid times, duplicate paths, and copy failures clearly.

## Learning Focus

- working with `pathlib` paths,
- copying folders with `shutil.copytree`,
- generating timestamped folder names,
- validating local file-system input,
- scheduling repeated jobs with `schedule`,
- keeping copy logic separate from terminal and scheduler logic.

## Run Command

From the repository root:

```powershell
python projects/18_automated_file_backup/src/automated_file_backup.py
```

## Expected Terminal Behavior

A valid run should ask for source and destination folders, then either run a backup immediately or schedule a daily backup.

Invalid folders, invalid schedule times, same source/destination paths, and copy failures should be handled with clear messages.

## Completion Checklist

- The program can be run from the terminal.
- Source and destination paths are validated.
- The destination folder is created when needed.
- Backup folders use timestamped names.
- Folder copying uses `shutil.copytree`.
- Scheduled mode uses `schedule` without running at import time.
- Automated tests mock time, scheduling, and file copying where practical.

## Notes

- Runtime source and backup folders are local practice data and should stay out of version control.
- The first version focuses on local folders only.
- Cloud backup, compression, encryption, and incremental backup are intentionally out of scope.
- Automated tests cover path validation, timestamped backup paths, folder copying, scheduler setup, and terminal flow.
