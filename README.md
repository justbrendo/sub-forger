# Sub-Forger

## Team Members
- Brendo Gético Eugênio
- Henrique Lucas Gomes Rezende
- Rodrigo Reis
- Samuel Lipovetsky

## System Overview
Sub-Forger is an automated subtitle burner for videos posted on YouTube. The system is divided into four main components:

### Video Download
The system downloads the YouTube video using the [pytube](https://pytube.io/en/latest/) library, ensuring fast speed downloads.

### Audio Extraction
Once the video is downloaded, the audio is separated from the video and converted to an appropriate format using [ffmpeg](https://ffmpeg.org/)

### Subtitle Generation
The audio file is then processed to generate accurate subtitles. This step utilizes the sophisticated speech-to-text library [faster-whiser](https://github.com/SYSTRAN/faster-whisper) to ensure high precision and seamless syncronization.

### Burning Subtitles onto the Video
Finally, the generated subtitles are burned onto the video, using again [ffmpeg](https://ffmpeg.org/)

## Technologies Used
### Pytest
[Pytest](https://docs.pytest.org/en/stable/) is a robust testing framework for Python applications. It supports simple unit tests as well as complex functional testing, making it an essential tool for ensuring code quality and reliability.

### FFmpeg
[FFmpeg](https://ffmpeg.org/) is a powerful multimedia framework used to handle audio, video, and other multimedia files and streams. It's used for video downloading, audio extraction, and embedding subtitles into videos.

### Faster-Whisper
[Faster-Whisper](https://github.com/guillaumekln/faster-whisper) is an optimized implementation of OpenAI's Whisper model for faster inference. It enhances the speed of speech-to-text processing without sacrificing accuracy.

### Whisper
[Whisper](https://github.com/openai/whisper) is a speech recognition model developed by OpenAI. It converts audio into text, providing highly accurate transcription which is essential for generating subtitles.

### Pytube
[Pytube](https://pytube.io/en/latest/) is a lightweight, Pythonic library for downloading YouTube videos. It simplifies the process of obtaining video files for subtitle processing.

### Coverage.py
Coverage.py is a measurement tool for code coverage of Python programs. It instruments the code to track which lines are executed during tests, providing valuable insights into the quality and comprehensiveness of a test suite.

## Contributing
We welcome contributions from the community!

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

Stay tuned for more updates and features!
