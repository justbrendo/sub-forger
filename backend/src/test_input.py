import os
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from main import *


@pytest.mark.parametrize(
    "title, max_title_size, expected_folder",
    [
        ("example_title", 10, "downloads/example_ti"),
        ("long_title_example", 5, "downloads/long_"),
        ("short", 10, "downloads/short"),
        ("precise_size", 12, "downloads/precise_size"),
    ],
)
def test_get_download_folder(title, max_title_size, expected_folder):
    assert get_download_folder(title, max_title_size) == expected_folder


@pytest.mark.parametrize(
    "download_folder, media, file_format, expected_path",
    [
        ("downloads", "video", "mp4", os.path.abspath("downloads/video.mp4")),
        (
            "other_downloads",
            "audio",
            "mp3",
            os.path.abspath("other_downloads/audio.mp3"),
        ),
        (
            "/home/user/downloads",
            "document",
            "pdf",
            "/home/user/downloads/document.pdf",
        ),
        (
            "/home/downloads",
            "audio",
            "mp3",
            "/home/downloads/audio.mp3",
        ),
    ],
)
def test_get_format_path(download_folder, media, file_format, expected_path):
    assert get_format_path(download_folder, media, file_format) == expected_path


@pytest.mark.parametrize(
    "url, expected_result",
    [
        ("https://www.youtube.com/watch?v=video_id", True),
        ("https://www.youtube.com/watch", False),
        ("www.youtube.com/watch?v=video_id", True),
        ("http://www.youtube.com/watch?v=video_id", True),
        ("https://example.com", False),
        ("https://www.m.youtube.com/watch?v=video_id", False),
        ("youtube.com/watch?v=video_id", True),
        ("/watch?v=video_id", False),
        ("invalid_url", False),
        ("https://www.m.youtube.com/watch?v=video_id/app=mobile", False),
        ("http://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s", True),
     
    ],
)
def test_is_valid_url(url, expected_result):
    assert is_valid_url(url) == expected_result


@pytest.mark.parametrize(
    "language_code, expected_result",
    [
        ("EN", True),
        ("en", True),
        ("la", False),
        ("LA", False),
        ("", False),
    ],
)
def test_is_valid_language_code(language_code, expected_result):
    assert is_valid_language_code(language_code) == expected_result


def test_get_download_folder_empty_title():
    with pytest.raises(ValueError, match="Title cannot be empty"):
        get_download_folder("", 10)


def test_get_download_folder_negative_max_title_size():
    with pytest.raises(ValueError, match="max_title_size must be greater than 0"):
        get_download_folder("my_title", -5)


def test_parse_arguments_valid():

    args = ["main.py", "https://www.youtube.com/watch?v=HKTyOUx9Wf4", "en", "large-v3"]
    expected_result = ("https://www.youtube.com/watch?v=HKTyOUx9Wf4", "en", "large-v3")
    assert parse_arguments(args) == expected_result


def test_parse_arguments_invalid_too_few_args():

    args = ["main.py"]
    with pytest.raises(
        ValueError,
    ):
        parse_arguments(args)


def test_parse_arguments_invalid_too_many_args():

    args = [
        "main.py",
        "https://www.youtube.com/watch?v=HKTyOUx9Wf4",
        "en",
        "small",
        "extra_arg",
    ]
    with pytest.raises(ValueError):
        parse_arguments(args)


def test_get_format_path_empty_folder():
    with pytest.raises(ValueError, match="Download folder cannot be empty"):
        get_format_path("", "my_media", "mp4")


def test_get_format_path_empty_media():
    with pytest.raises(ValueError, match="Media cannot be empty"):
        get_format_path("downloads", "", "mp4")


def test_get_format_path_empty_format():
    with pytest.raises(ValueError):
        get_format_path("downloads", "my_media", "")

    