import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock, patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "projects"
    / "17_youtube_video_downloader"
    / "src"
    / "youtube_video_downloader.py"
)


def load_youtube_video_downloader() -> ModuleType:
    spec = importlib.util.spec_from_file_location("youtube_downloader_under_test", SCRIPT)
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


def test_module_import_does_not_prompt_open_dialog_or_create_youtube() -> None:
    with (
        patch("builtins.input") as input_mock,
        patch("tkinter.Tk") as tk_mock,
        patch("pytubefix.YouTube") as youtube_mock,
    ):
        load_youtube_video_downloader()

    input_mock.assert_not_called()
    tk_mock.assert_not_called()
    youtube_mock.assert_not_called()


def test_choose_download_folder_uses_hidden_dialog_and_destroys_root() -> None:
    downloader = load_youtube_video_downloader()
    root = Mock()

    with (
        patch.object(downloader, "Tk", return_value=root),
        patch.object(
            downloader.filedialog,
            "askdirectory",
            return_value="D:\\Downloads",
        ) as askdirectory,
    ):
        folder = downloader.choose_download_folder()

    assert folder == "D:\\Downloads"
    root.withdraw.assert_called_once_with()
    askdirectory.assert_called_once_with(title="Choose download folder")
    root.destroy.assert_called_once_with()


def test_choose_download_folder_destroys_root_when_dialog_fails() -> None:
    downloader = load_youtube_video_downloader()
    root = Mock()

    with (
        patch.object(downloader, "Tk", return_value=root),
        patch.object(
            downloader.filedialog,
            "askdirectory",
            side_effect=RuntimeError("dialog failed"),
        ),
    ):
        with pytest.raises(RuntimeError, match="dialog failed"):
            downloader.choose_download_folder()

    root.destroy.assert_called_once_with()


def test_select_video_stream_uses_progressive_mp4_highest_resolution() -> None:
    downloader = load_youtube_video_downloader()
    youtube = Mock()
    filtered_streams = Mock()
    selected_stream = Mock()

    youtube.streams.filter.return_value = filtered_streams
    filtered_streams.get_highest_resolution.return_value = selected_stream

    stream = downloader.select_video_stream(youtube)

    assert stream is selected_stream
    youtube.streams.filter.assert_called_once_with(progressive=True, file_extension="mp4")
    filtered_streams.get_highest_resolution.assert_called_once_with()


def test_download_video_returns_downloaded_file_path() -> None:
    downloader = load_youtube_video_downloader()
    stream = Mock()
    stream.download.return_value = "D:\\Downloads\\sample.mp4"

    file_path = downloader.download_video(stream, "D:\\Downloads")

    assert file_path == "D:\\Downloads\\sample.mp4"
    stream.download.assert_called_once_with(output_path="D:\\Downloads")


def test_main_handles_empty_url_without_opening_folder_picker() -> None:
    downloader = load_youtube_video_downloader()

    with patch.object(downloader, "choose_download_folder") as choose_download_folder:
        _, output = call_with_inputs(downloader.main, ["   "])

    choose_download_folder.assert_not_called()
    assert output == "Enter YouTube video URL: Video URL cannot be empty.\n"


def test_main_handles_cancelled_folder_without_creating_youtube() -> None:
    downloader = load_youtube_video_downloader()

    with (
        patch.object(downloader, "choose_download_folder", return_value=""),
        patch.object(downloader, "create_youtube") as create_youtube,
    ):
        _, output = call_with_inputs(
            downloader.main,
            ["https://www.youtube.com/watch?v=NpmFbWO6HPU"],
        )

    create_youtube.assert_not_called()
    assert output.endswith("No download folder selected.\n")


def test_main_handles_no_downloadable_stream() -> None:
    downloader = load_youtube_video_downloader()
    youtube = Mock()

    with (
        patch.object(downloader, "choose_download_folder", return_value="D:\\Downloads"),
        patch.object(downloader, "create_youtube", return_value=youtube),
        patch.object(downloader, "select_video_stream", return_value=None),
        patch.object(downloader, "download_video") as download_video,
    ):
        _, output = call_with_inputs(
            downloader.main,
            ["https://www.youtube.com/watch?v=NpmFbWO6HPU"],
        )

    download_video.assert_not_called()
    assert output.endswith("No downloadable MP4 stream found.\n")


def test_main_downloads_selected_stream_successfully() -> None:
    downloader = load_youtube_video_downloader()
    youtube = Mock()
    stream = Mock()
    youtube.title = "Sample Video"

    with (
        patch.object(downloader, "choose_download_folder", return_value="D:\\Downloads"),
        patch.object(downloader, "create_youtube", return_value=youtube),
        patch.object(downloader, "select_video_stream", return_value=stream),
        patch.object(
            downloader,
            "download_video",
            return_value="D:\\Downloads\\sample.mp4",
        ) as download_video,
    ):
        _, output = call_with_inputs(
            downloader.main,
            ["https://www.youtube.com/watch?v=NpmFbWO6HPU"],
        )

    download_video.assert_called_once_with(stream, "D:\\Downloads")
    assert "Downloading: Sample Video" in output
    assert "Downloaded successfully: D:\\Downloads\\sample.mp4" in output


def test_main_handles_video_unavailable_and_download_errors() -> None:
    downloader = load_youtube_video_downloader()

    with (
        patch.object(downloader, "choose_download_folder", return_value="D:\\Downloads"),
        patch.object(
            downloader,
            "create_youtube",
            side_effect=downloader.VideoUnavailable("abc123"),
        ),
    ):
        _, unavailable_output = call_with_inputs(
            downloader.main,
            ["https://www.youtube.com/watch?v=NpmFbWO6HPU"],
        )

    with (
        patch.object(downloader, "choose_download_folder", return_value="D:\\Downloads"),
        patch.object(downloader, "create_youtube", side_effect=RuntimeError("failed")),
    ):
        _, generic_error_output = call_with_inputs(
            downloader.main,
            ["https://www.youtube.com/watch?v=NpmFbWO6HPU"],
        )

    assert downloader.DOWNLOAD_ERROR_MESSAGE in unavailable_output
    assert downloader.DOWNLOAD_ERROR_MESSAGE in generic_error_output
