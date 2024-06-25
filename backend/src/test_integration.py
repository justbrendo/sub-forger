import os
import unittest
import wave
from utils import Transcriber
from main import DownloadThumbnailCommand, DownloadVideoCommand
from pytube import YouTube

class TranscriberIntegrationTests(unittest.TestCase):

    def setUp(self):
        # Create a valid WAV file for testing
        self.wav_path = "test.wav"
        self.create_valid_wav(self.wav_path)

        self.download_folder = "/tmp/test"
        os.makedirs(self.download_folder, exist_ok=True)

    def tearDown(self):
        # Clean up the test WAV file and any generated SRT files
        if os.path.exists(self.wav_path):
            os.remove(self.wav_path)

        srt_path = os.path.join(self.download_folder, "subs.srt")
        if os.path.exists(srt_path):
            os.remove(srt_path)

    def create_valid_wav(self, filename):
        with wave.open(filename, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            wf.writeframes(b'\x00\x00' * 44100)

    def test_transcribe_successful(self):
        video_length_in_seconds = 10
        model_name = "tiny"
        language_code = "en"

        transcriber = Transcriber(self.wav_path, self.download_folder, video_length_in_seconds, model_name, language_code)
        transcriber.execute()

        srt_path = os.path.join(self.download_folder, "subs.srt")
        self.assertTrue(os.path.exists(srt_path))
        with open(srt_path, "r") as f:
            content = f.read()
        self.assertIn("1", content)

    def test_transcribe_with_empty_wav_path(self):
        wav_path = ""
        video_length_in_seconds = 10
        model_name = "tiny"
        language_code = "en"

        transcriber = Transcriber(wav_path, self.download_folder, video_length_in_seconds, model_name, language_code)

        with self.assertRaises(Exception):
            transcriber.execute()
        srt_path = os.path.join(self.download_folder, "subs.srt")
        self.assertFalse(os.path.exists(srt_path))    

class DownloadThumbnailIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.download_folder = "/tmp/test_thumbnail"
        os.makedirs(self.download_folder, exist_ok=True)

    def tearDown(self):
        thumbnail_path = os.path.join(self.download_folder, "thumbnail.jpg")
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)

    def test_download_thumbnail_successful(self):
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
        yt = YouTube(video_url)

        command = DownloadThumbnailCommand(download_folder=self.download_folder, video_url=video_url)
        command.execute(yt)

        thumbnail_path = os.path.join(self.download_folder, "thumbnail.jpg")
        self.assertTrue(os.path.exists(thumbnail_path))

class DownloadVideoIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.download_folder = "/tmp/test_video"
        os.makedirs(self.download_folder, exist_ok=True)

    def tearDown(self):
        video_path = os.path.join(self.download_folder, "video.mp4")
        if os.path.exists(video_path):
            os.remove(video_path)

    def test_download_video_successful(self):
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
        yt = YouTube(video_url)

        command = DownloadVideoCommand(download_folder=self.download_folder)
        command.execute(yt)

        video_path = os.path.join(self.download_folder, "video.mp4")
        self.assertTrue(os.path.exists(video_path))
    
    def test_download_video_to_nonexistent_folder(self):
        download_folder = "/nonexistent_folder"
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
        yt = YouTube(video_url)

        command = DownloadVideoCommand(download_folder=download_folder)
        with self.assertRaises(Exception):
            command.execute(yt)

if __name__ == "__main__":
    unittest.main()
