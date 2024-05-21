import os
import re
import sys
import urllib.request

import ffmpeg
from pytube import YouTube
from pytube.innertube import _default_clients
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

from utils import Transcriber

MAX_TITLE_SIZE = 100

def download_video(url, resolution='1440p'):
    """
    Downloads the YouTube video at the specified resolution or the best available quality up to that resolution.
    
    Parameters:
    - url: str, the URL of the YouTube video
    - resolution: str, the target resolution
    
    Returns:
    - str, the path to the downloaded video file's folder
    - str, the path to the downloaded video file
    - str, the title of the video
    - int, the length of the video in seconds
    """
    yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
    
    # Filter streams by resolution and progressive download (video+audio)
    streams = yt.streams.filter(progressive=True, file_extension='mp4')
    
    # Get the best stream at or below the desired resolution
    stream = streams.filter(res=resolution).first() or streams.order_by('resolution').desc().first()
    
    if not stream:
        raise ValueError(f"No suitable streams found for resolution {resolution}")
    
    print(f"Downloading: {stream.title} at {stream.resolution}")
    download_folder = f"downloads/{stream.title[:MAX_TITLE_SIZE]}"
    stream.download(output_path=f'{download_folder}', filename='video.mp4')
    print(f"{yt.title} has been downloaded successfully")
    
    return download_folder, download_folder + "/video.mp4", yt.title, yt.length


def download_thumbnail(video_url, download_folder):
    """
    Downloads the thumbnail of a YouTube video.

    Parameters:
    - video_url: str, the URL of the YouTube video
    - download_folder: str, the folder where the thumbnail will be saved
    
    Returns:
    - str, the path to the downloaded thumbnail file
    """
    yt = YouTube(video_url, use_oauth=False, allow_oauth_cache=False)
    thumbnail_file_path = f"{download_folder}/thumbnail.jpg"
    urllib.request.urlretrieve(yt.thumbnail_url, thumbnail_file_path)
    print(f"{yt.title} thumbnail has been downloaded successfully")
    return thumbnail_file_path


def convert_video_to_audio(video_file_path, download_folder, yt_title):
    """
    Converts a video file to MP3 and WAV audio formats.

    Parameters:
    - video_file_path: str, path to the video file
    - download_folder: str, the folder where the audio files will be saved
    - yt_title: str, the title of the YouTube video for logging purposes
    
    Returns:
    - tuple, paths to the converted MP3 and WAV files
    """
    mp3_path = f"{download_folder}/audio.mp3"
    wav_path = f"{download_folder}/audio.wav"

    ffmpeg.input(video_file_path).output(mp3_path).run(overwrite_output=True)
    print(f"{yt_title} has been converted to mp3 successfully")
    
    ffmpeg.input(video_file_path).output(wav_path, ar="16000").run(overwrite_output=True)
    print(f"{yt_title} has been converted to wav successfully")
    
    return mp3_path, wav_path


def burn_subtitles(video_path, subtitle_path, output_path):
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
            ffmpeg
            .input(video_path)
            .output(output_path, vf=f'subtitles={subtitle_path}', vcodec='libx264', acodec='copy')
            .run(overwrite_output=True)
        )
        print(f"Subtitles burned successfully into {output_path}")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")
        
        
def main():
    # Check if sys.argv[1] is provided
    if len(sys.argv) < 4:
        print("Error: You need to provide a valid URL")
        print("Usage: python main.py <URL> <LANGUAGE_CODE> <MODEL_NAME>")
        sys.exit(1)
    
    # Download the video
    download_folder, video_file_path, yt_title, yt_length = download_video(sys.argv[1])

    # Download the thumbnail
    thumbnail_file_path =download_thumbnail(sys.argv[1], download_folder)
    
    # Convert the video to mp3 and wav
    mp3_path, wav_path = convert_video_to_audio(video_file_path, download_folder, yt_title)
    
    # Set the model name and language code
    MODEL_NAME = sys.argv[3]
    LANGUAGE_CODE = sys.argv[2]
    
    # Transcribe the audio using Whisper
    transcriber = Transcriber(wav_path, download_folder, yt_length, MODEL_NAME, LANGUAGE_CODE)
    srt_path = transcriber.transcribe()
    
    # Burn the subtitles into the video
    burn_subtitles(video_file_path, srt_path, f'{download_folder}/burned_video.mp4')
    
if __name__ == "__main__":
    main()