import os
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from utils import Transcriber
from collections import namedtuple




@pytest.mark.parametrize("seconds, always_include_hours, expected_result", [
    (0, False, "00:00,000"),
    (0, True, "00:00:00,000"),
    (65, False, "01:05,000"),
    (65, True, "00:01:05,000"),
    (3600, False, "01:00:00,000"),
    (3600, True, "01:00:00,000"),
    (3665.123, False, "01:01:05,123"),
    (3665.123, True, "01:01:05,123"),
    (86400, False, "24:00:00,000"),
    (86400, True, "24:00:00,000"),
])
def test_format_timestamp(seconds, always_include_hours, expected_result):
    trans= Transcriber(None,None,None,None,None)
    assert trans.format_timestamp(seconds, always_include_hours) == expected_result
    
def test_format_timestamp_negative_seconds():
    trans = Transcriber(None, None, None, None, None)
    with pytest.raises(AssertionError):
        trans.format_timestamp(-1, False)

def test_format_timestamp_large_seconds():
    trans = Transcriber(None, None, None, None, None)
    assert trans.format_timestamp(9999999999.999, True) == "2777777:46:39,999"
    
Segment = namedtuple("Segment", ["start", "end", "text"])
@pytest.fixture
def mock_transcript():
    # Mock transcript data
    return [
        Segment(start=0, end=10, text="Hello"),
        Segment(start=10, end=20, text="World"),
    ]
def test_write_srt_with_mocked_print_and_progress_bar(mock_transcript, capsys):
    class MockProgressBar:
        def update(self, value):
            self.value = value

    transcriber = Transcriber(None,None,None,None,None)  
    transcriber.format_timestamp = lambda seconds, always_include_hours: f"00:00:{seconds},000"  
    pbar = MockProgressBar()  
    transcriber.write_srt(mock_transcript, file=None, pbar=pbar)
    assert pbar.value == 10  

