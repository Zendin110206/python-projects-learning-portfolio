# Project 17 - YouTube Video Downloader

Status: Completed.

This project is a command-line YouTube video downloader with a local folder picker. It is intended for practicing third-party libraries, stream selection, GUI file dialogs, path handling, and defensive error handling around external services.

## Goal

Build a small program that:

- asks for a YouTube video URL,
- lets the user choose a local download folder,
- reads video metadata through a Python library,
- selects a progressive MP4 stream,
- downloads the selected stream,
- handles invalid URLs, unavailable videos, cancelled folders, and missing streams clearly.

## Learning Focus

- using `pytubefix` to work with YouTube video metadata and streams,
- using `tkinter.filedialog` to choose a local folder,
- separating user prompts, folder selection, stream selection, and download logic,
- avoiding tracebacks for normal runtime failures,
- testing downloader logic with mocks instead of downloading live videos.

## Run Command

From the repository root:

```powershell
python projects/17_youtube_video_downloader/src/youtube_video_downloader.py
```

## Expected Terminal Behavior

A valid run should ask for a video URL, open a folder picker, show which video is being downloaded, and then print the saved file path.

Invalid URLs, unavailable videos, cancelled folder selection, missing downloadable MP4 streams, and download failures should be handled with clear messages.

## Completion Checklist

- The program can be run from the terminal.
- The URL prompt is clear.
- Folder selection can be cancelled safely.
- A progressive MP4 stream is selected.
- Downloads are saved to the selected folder.
- Library and download failures are handled without tracebacks.
- Automated tests mock `pytubefix` and the folder picker instead of downloading live videos.

## Notes

- The first version uses `pytubefix` instead of the older `pytube` package.
- Downloaded video files are local runtime output and should stay out of version control.
- This exercise is intended only for videos the user owns or has permission to download.
- Automated tests mock the YouTube object, stream selection, and folder picker.
