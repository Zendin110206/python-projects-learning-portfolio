import shutil
import time
from datetime import datetime
from pathlib import Path

import schedule

SOURCE_MISSING_MESSAGE = "Source folder does not exist."
BACKUP_EMPTY_MESSAGE = "Backup folder cannot be empty."
SAME_FOLDER_MESSAGE = "Source and backup folders must be different."
INVALID_TIME_MESSAGE = "Invalid time. Please use HH:MM."
BACKUP_ERROR_MESSAGE = "Backup failed. Please check the folders and try again."
SCHEDULER_STOPPED_MESSAGE = "Backup scheduler stopped."


def parse_folder_path(folder_path):
    folder_path = folder_path.strip()

    if not folder_path:
        return None

    return Path(folder_path)


def validate_source_folder(source_path):
    if source_path is None or not source_path.exists() or not source_path.is_dir():
        return False

    return True


def validate_backup_folder(backup_root):
    if backup_root is None:
        return False

    return True


def folders_are_same(source_path, backup_root):
    if source_path.resolve() == backup_root.resolve():
        return True

    return False


def create_backup_path(backup_root, now=None):
    if now is None:
        now = datetime.now()

    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    return backup_root / f"backup_{timestamp}"


def copy_folder(source_path, backup_path):
    shutil.copytree(source_path, backup_path)

    return backup_path


def run_backup_job(source_path, backup_root):
    backup_root.mkdir(parents=True, exist_ok=True)
    backup_path = create_backup_path(backup_root)

    try:
        copy_folder(source_path, backup_path)
        print(f"Backup created: {backup_path}")
        return backup_path

    except Exception:
        print(BACKUP_ERROR_MESSAGE)
        return None


def is_valid_backup_time(backup_time):
    if len(backup_time) != 5:
        return False

    if backup_time[2] != ":":
        return False

    try:
        datetime.strptime(backup_time, "%H:%M")
        return True
    except ValueError:
        return False


def start_scheduler(source_path, backup_root, backup_time):
    schedule.every().day.at(backup_time).do(run_backup_job, source_path, backup_root)
    print(f"Scheduled daily backup at {backup_time}. Press Ctrl+C to stop.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print(SCHEDULER_STOPPED_MESSAGE)


def main():
    source_text = input("Enter source folder: ").strip()
    backup_text = input("Enter backup folder: ").strip()
    backup_time = input("Enter backup time (HH:MM) or press Enter to run now: ").strip()

    source_path = parse_folder_path(source_text)
    backup_root = parse_folder_path(backup_text)

    if not validate_source_folder(source_path):
        print(SOURCE_MISSING_MESSAGE)
        return

    if not validate_backup_folder(backup_root):
        print(BACKUP_EMPTY_MESSAGE)
        return

    if folders_are_same(source_path, backup_root):
        print(SAME_FOLDER_MESSAGE)
        return

    if not backup_time:
        run_backup_job(source_path, backup_root)
        return

    if not is_valid_backup_time(backup_time):
        print(INVALID_TIME_MESSAGE)
        return

    start_scheduler(source_path, backup_root, backup_time)


if __name__ == "__main__":
    main()
