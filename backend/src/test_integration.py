import os
import wave
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from utils import Transcriber
from main import DownloadThumbnailCommand, DownloadVideoCommand
from pytube import YouTube

@pytest.fixture
def create_valid_wav():
    wav_path = "test.wav"
    with wave.open(wav_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b'\x00\x00' * 44100)
    yield wav_path
    if os.path.exists(wav_path):
        os.remove(wav_path)

@pytest.fixture
def create_download_folder():
    download_folder = "/tmp/test"
    os.makedirs(download_folder, exist_ok=True)
    yield download_folder
    if os.path.exists(download_folder):
        for file in os.listdir(download_folder):
            os.remove(os.path.join(download_folder, file))
        os.rmdir(download_folder)

def test_transcribe_successful(create_valid_wav, create_download_folder):
    video_length_in_seconds = 10
    model_name = "tiny"
    language_code = "en"

    transcriber = Transcriber(create_valid_wav, create_download_folder, video_length_in_seconds, model_name, language_code)
    transcriber.execute()

    srt_path = os.path.join(create_download_folder, "subs.srt")
    assert os.path.exists(srt_path)
    with open(srt_path, "r") as f:
        content = f.read()
    assert "1" in content

def test_transcribe_with_empty_wav_path(create_download_folder):
    wav_path = ""
    video_length_in_seconds = 10
    model_name = "tiny"
    language_code = "en"

    transcriber = Transcriber(wav_path, create_download_folder, video_length_in_seconds, model_name, language_code)

    with pytest.raises(Exception):
        transcriber.execute()
    srt_path = os.path.join(create_download_folder, "subs.srt")
    assert not os.path.exists(srt_path)

@pytest.fixture
def create_thumbnail_folder():
    download_folder = "/tmp/test_thumbnail"
    os.makedirs(download_folder, exist_ok=True)
    yield download_folder
    thumbnail_path = os.path.join(download_folder, "thumbnail.jpg")
    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
    os.rmdir(download_folder)

def test_download_thumbnail_successful(create_thumbnail_folder):
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
    yt = YouTube(video_url)

    command = DownloadThumbnailCommand(download_folder=create_thumbnail_folder, video_url=video_url)
    command.execute(yt)

    thumbnail_path = os.path.join(create_thumbnail_folder, "thumbnail.jpg")
    assert os.path.exists(thumbnail_path)

@pytest.fixture
def create_video_folder():
    download_folder = "/tmp/test_video"
    os.makedirs(download_folder, exist_ok=True)
    yield download_folder
    video_path = os.path.join(download_folder, "video.mp4")
    if os.path.exists(video_path):
        os.remove(video_path)
    os.rmdir(download_folder)

def test_download_video_successful(create_video_folder):
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
    yt = YouTube(video_url)

    command = DownloadVideoCommand(download_folder=create_video_folder)
    command.execute(yt)

    video_path = os.path.join(create_video_folder, "video.mp4")
    assert os.path.exists(video_path)

def test_download_video_to_nonexistent_folder():
    download_folder = "/nonexistent_folder"
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
    yt = YouTube(video_url)

    command = DownloadVideoCommand(download_folder=download_folder)
    with pytest.raises(Exception):
        command.execute(yt)

if __name__ == "__main__":
    pytest.main()
