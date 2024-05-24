import os
import re
import sys
import urllib.request

import ffmpeg
from pytube import YouTube
from pytube.innertube import _default_clients

from utils import Transcriber

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

MAX_TITLE_SIZE = 100


class Command:
    def execute(self, yt):
        pass


class DownloadVideoCommand(Command):
    def __init__(self, download_folder, resolution="720p"):
        self.download_folder = download_folder
        self.resolution = resolution

    def execute(self, yt):
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        stream = (
                streams.filter(res="720p").first()
                or streams.order_by("resolution").desc().first()
        )
        if not stream:
            raise ValueError(
                f"No suitable streams found for resolution {self.resolution}"
            )

        print(f"Downloading: {stream.title} at {stream.resolution}")
        stream.download(output_path=f"{self.download_folder}", filename="video.mp4")
        print(f"{yt.title} has been downloaded successfully")
        return (
            self.download_folder,
            self.download_folder + "/video.mp4",
            yt.title,
            yt.length,
            stream.resolution,
        )


class DownloadThumbnailCommand(Command):
    def __init__(self, download_folder, video_url):
        self.download_folder = download_folder
        self.video_url = video_url

    def execute(self, yt):
        """
        Downloads the thumbnail of a YouTube video.

        Parameters:
        - video_url: str, the URL of the YouTube video
        - download_folder: str, the folder where the thumbnail will be saved

        Returns:
        - str, the path to the downloaded thumbnail file
        """
        yt = YouTube(self.video_url, use_oauth=False, allow_oauth_cache=False)

        thumbnail_file_path = self.download_folder + "/thumbnail.jpg"

        urllib.request.urlretrieve(yt.thumbnail_url, thumbnail_file_path)
        print(f"{yt.title} thumbnail has been downloaded successfully")
        return thumbnail_file_path


class ConvertVideoToAudioCommand(Command):
    def __init__(
            self,
            video_file_path,
            download_folder,
    ):
        self.video_file_path = video_file_path
        self.download_folder = download_folder

    def execute(self, yt):
        """
        Converts a video file to MP3 and WAV audio formats.

        Returns:
        - tuple, paths to the converted MP3 and WAV files
        """
        mp3_path = f"{self.download_folder}/audio.mp3"
        wav_path = f"{self.download_folder}/audio.wav"

        ffmpeg.input(self.video_file_path).output(mp3_path).run(overwrite_output=True)
        print(f"{yt.title} has been converted to mp3 successfully")

        ffmpeg.input(self.video_file_path).output(wav_path, ar="16000").run(
            overwrite_output=True
        )
        print(f"{yt.title} has been converted to wav successfully")

        return mp3_path, wav_path


class BurnSubtitlesCommand(Command):
    def __init__(self, video_file_path, subtitle_path, output_path):
        self.video_file_path = video_file_path
        self.subtitle_path = subtitle_path
        self.output_path = output_path

    def execute(self, yt=None):
        """
        Burns subtitles from an SRT file into an MP4 video using ffmpeg-python.

        Parameters:
        - video_path: str, path to the input video file
        - subtitle_path: str, path to the subtitle file (SRT)
        - output_path: str, path to save the output video file
        """
        try:
            # Build the FFmpeg command using ffmpeg-python
            (
                ffmpeg.input(self.video_file_path)
                .output(
                    self.output_path,
                    vf=f"subtitles={self.subtitle_path}",
                    vcodec="libx264",
                    acodec="copy",
                )
                .run(overwrite_output=True)
            )
            print(f"Subtitles burned successfully into {self.output_path}")
        except ffmpeg.Error as e:
            print(f"An error occurred: {e.stderr.decode()}")


def get_download_folder(title, max_title_size):
    if not title:
        raise ValueError("Title cannot be empty")
    if max_title_size <= 0:
        raise ValueError("max_title_size must be greater than 0")
    return f"downloads/{title[:max_title_size]}"


def get_format_path(download_folder, media, file_format):
    if not download_folder:
        raise ValueError("Download folder cannot be empty")
    if not media:
        raise ValueError("Media cannot be empty")
    if not file_format:
        raise ValueError("File format cannot be empty")
    return download_folder + "/" + media + "." + file_format



def main():
    # Check if sys.argv[1] is provided
    if len(sys.argv) < 4:
        print("Error: You need to provide a valid URL")
        print("Usage: python main.py <URL> <LANGUAGE_CODE> <MODEL_NAME>")
        sys.exit(1)
    # parsing and validating arguments
    url = sys.argv[1]
    language_code = sys.argv[2]
    model_name = sys.argv[3]

    yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
    yt_title = yt.title
    yt_length = yt.length
    download_folder = get_download_folder(yt_title, MAX_TITLE_SIZE)
    video_file_path = get_format_path(
        download_folder=download_folder, media="video", file_format="mp4"
    )
    wav_path = get_format_path(
        download_folder=download_folder, media="audio", file_format="wav"
    )
    srt_path = get_format_path(
        download_folder=download_folder, media="subs", file_format="srt"
    )
    output_video_path = get_format_path(
        download_folder=download_folder, media="burned_video", file_format="mp4"
    )

    # making commands
    commands = [
        DownloadVideoCommand(download_folder=download_folder),
        DownloadThumbnailCommand(download_folder=download_folder, video_url=url),
        ConvertVideoToAudioCommand(
            video_file_path=video_file_path,
            download_folder=download_folder,

        ),
        Transcriber(wav_path, download_folder, yt_length, model_name, language_code),
        BurnSubtitlesCommand(
            video_file_path=video_file_path,
            subtitle_path=srt_path,
            output_path=output_video_path,
        ),
    ]

    # executing commands
    for command in commands:
        command.execute(yt=yt)


if __name__ == "__main__":
    main()
