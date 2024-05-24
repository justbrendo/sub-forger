import unittest
from main import get_download_folder, get_format_path


class TestDownloadFunctions(unittest.TestCase):

    def test_get_download_folder_within_max_size(self):
        # Test when title is within max size
        self.assertEqual(get_download_folder("my_title", 10), "downloads/my_title")

    def test_get_download_folder_long_title(self):
        # Test when title is longer than max size
        self.assertEqual(get_download_folder("a_very_long_title", 10), "downloads/a_very_lon")

    def test_get_download_folder_empty_title(self):
        # Test when title is empty
        with self.assertRaises(ValueError):
            get_download_folder("", 10)

    def test_get_download_folder_negative_max_title_size(self):
        # Test when max_title_size is negative
        with self.assertRaises(ValueError):
            get_download_folder("my_title", -5)

    def test_get_download_folder_zero_max_title_size(self):
        # Test when max_title_size is zero
        with self.assertRaises(ValueError):
            get_download_folder("my_title", 0)

    def test_get_format_path_valid_inputs(self):
        # Test when download folder, media, and file format are provided
        self.assertEqual(get_format_path("downloads", "my_media", "mp4"), "downloads/my_media.mp4")

    def test_get_format_path_empty_folder(self):
        # Test when download folder is empty
        with self.assertRaises(ValueError):
            get_format_path("", "my_media", "mp4")

    def test_get_format_path_empty_media(self):
        # Test when media is empty
        with self.assertRaises(ValueError):
            get_format_path("downloads", "", "mp4")

    def test_get_format_path_empty_format(self):
        # Test when file format is empty
        with self.assertRaises(ValueError):
            get_format_path("downloads", "my_media", "")

            
if __name__ == '__main__':
    unittest.main()
