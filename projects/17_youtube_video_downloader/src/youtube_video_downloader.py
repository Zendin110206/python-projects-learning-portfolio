from tkinter import Tk, filedialog

from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable

EMPTY_URL_MESSAGE = "Video URL cannot be empty."
NO_FOLDER_MESSAGE = "No download folder selected."
NO_STREAM_MESSAGE = "No downloadable MP4 stream found."
DOWNLOAD_ERROR_MESSAGE = "Download failed. Please check the URL and try again."


def choose_download_folder():
    root = Tk()
    try:
        root.withdraw()
        return filedialog.askdirectory(title="Choose download folder")
    finally:
        root.destroy()


def create_youtube(video_url):
    return YouTube(video_url)


def select_video_stream(youtube):
    streams = youtube.streams.filter(progressive=True, file_extension="mp4")
    return streams.get_highest_resolution()


def download_video(stream, download_folder):
    return stream.download(output_path=download_folder)


def main():
    video_url = input("Enter YouTube video URL: ").strip()

    if not video_url:
        print(EMPTY_URL_MESSAGE)
        return

    download_folder = choose_download_folder()

    if not download_folder:
        print(NO_FOLDER_MESSAGE)
        return

    try:
        youtube = create_youtube(video_url)
        stream = select_video_stream(youtube)

        if stream is None:
            print(NO_STREAM_MESSAGE)
            return

        print(f"Downloading: {youtube.title}")
        file_path = download_video(stream, download_folder)
        print(f"Downloaded successfully: {file_path}")

    except VideoUnavailable:
        print(DOWNLOAD_ERROR_MESSAGE)
    except Exception:
        print(DOWNLOAD_ERROR_MESSAGE)


if __name__ == "__main__":
    main()
