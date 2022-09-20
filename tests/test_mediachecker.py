import unittest
import os
from pathlib import Path

from mediachecker import AVFile

tests_dir = Path(__file__).parent


class TestMediaChecker(unittest.TestCase):
    def test_good_file_detection(self):
        f = AVFile(os.path.join(tests_dir, 'data', 'good_example.mp4'))
        self.assertTrue(f.is_good(method='first_audio_track'))
        self.assertTrue(f.is_good(method='full'))

    def test_bad_file_detection(self):
        f = AVFile(os.path.join(tests_dir, 'data', 'bad_example.mp4'))
        self.assertFalse(f.is_good(method='first_audio_track'))
        self.assertFalse(f.is_good(method='full'))

    def test_tricky_bad_file_detection(self):
        f = AVFile(os.path.join(tests_dir, 'data', 'tricky_example.mp4'))
        self.assertFalse(f.is_good(method='full'))

    def test_invalid_file_type(self):
        f = AVFile(os.path.join(tests_dir, 'data', 'invalid_example.txt'))
        with self.assertWarns(UserWarning) as cm:
            self.assertIsNone(f.is_good(method='first_audio_track'))
        with self.assertWarns(UserWarning) as cm:
            self.assertIsNone(f.is_good(method='full'))

    # TODO:
    # * test file with weird characters in the name
    # * test different media types, e.g. audio only, video only, ...
    # * test CLI script


if __name__ == '__main__':
    unittest.main()
