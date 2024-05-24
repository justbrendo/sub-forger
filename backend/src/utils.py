import os

import requests
import platform
from requests_toolbelt.multipart import MultipartEncoder
from tqdm import tqdm
import faster_whisper


class Transcriber:

    def __init__(self, wav_path, download_folder, video_length_in_seconds, model_name, language_code):
        self.wav_path = wav_path
        self.download_folder = download_folder
        self.video_length_in_seconds = video_length_in_seconds
        self.model_name = model_name
        self.language_code = language_code
        # Available models ⬇️
        self.models = ["tiny", "tiny.en", "base", "base.en",
                       "small", "small.en", "medium", "medium.en",
                       "large", "large-v1", "large-v2", "large-v3"]

    def is_model_available(self):
        # Checks if the selected model is available
        return self.model_name in self.models

    @staticmethod
    def format_timestamp(seconds: float, always_include_hours: bool = False):
        assert seconds >= 0, "non-negative timestamp expected"
        milliseconds = round(seconds * 1000.0)

        hours = milliseconds // 3_600_000
        milliseconds -= hours * 3_600_000

        minutes = milliseconds // 60_000
        milliseconds -= minutes * 60_000

        seconds = milliseconds // 1_000
        milliseconds -= seconds * 1_000

        hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
        return f"{hours_marker}{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    def write_srt(self, transcript, file, pbar=None):
        for chunk, segment in enumerate(transcript, start=1):
            print(
                f"{chunk}\n"
                f"{self.format_timestamp(segment.start, always_include_hours=True)} --> "
                f"{self.format_timestamp(segment.end, always_include_hours=True)}\n"
                f"{segment.text.strip().replace('-->', '->')}\n",
                file=file,
                flush=True,
            )
            # Update the progress bar
            if pbar:
                pbar.update(segment.end - segment.start)

    def execute(self, yt=None):
        if not self.is_model_available():
            print(f"Error: {self.model_name} is not available")
            exit(1)

        # Load model into memory
        model = faster_whisper.WhisperModel(
            self.model_name,
            device="cpu",  # cuda or cpu
            compute_type="int8",  # float16 or int8
            cpu_threads=16,
        )

        # Prepare the iterator for transcribing
        segments, _info = model.transcribe(self.wav_path, beam_size=8)

        # Initialize the progress bar
        pbar = tqdm(total=self.video_length_in_seconds, desc="Transcribing")

        # Effectively write the SRT file in real time whilst transcribing

        with open(f"{self.download_folder}/subs.srt", "w", encoding="utf-8") as srt:
            self.write_srt(segments, file=srt)

        # Close the progress bar
        pbar.close()

        return f"{self.download_folder}/subs.srt"
