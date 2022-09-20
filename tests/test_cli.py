import unittest
import os
from pathlib import Path

from mediachecker.cli import (
    check_file,
    check_path,
    find_files_nonrecursive,
    find_files_recursive,
)

tests_dir = Path(__file__).parent


class TestCLI(unittest.TestCase):

    # # Testing check_file() is (or should be) redundant with other tests:
    # def test_good_file_detection(self):
    #     filename = os.path.join(tests_dir, 'data', 'good_example.mp4')
    #     self.assertTrue(
    #         check_file(filename, write_log=False, method='first_audio_track')
    #     )
    #     self.assertTrue(
    #         check_file(filename, write_log=False, method='full')
    #     )
    # def test_bad_file_detection(self):
    #     filename = os.path.join(tests_dir, 'data', 'bad_example.mp4')
    #     self.assertFalse(
    #         check_file(filename, write_log=False, method='first_audio_track')
    #     )
    #     self.assertFalse(
    #         check_file(filename, write_log=False, method='full')
    #     )
    # def test_tricky_bad_file_detection(self):
    #     filename = os.path.join(tests_dir, 'data', 'tricky_example.mp4')
    #     self.assertFalse(
    #         check_file(filename, write_log=False, method='full')
    #     )

    def test_finding_no_files(self):
        base_dir = tests_dir
        matching_files = find_files_nonrecursive(base_dir, '*.mp4')
        self.assertEqual(len(matching_files), 0)

    def test_finding_files(self):
        base_dir = os.path.join(tests_dir, 'data')
        matching_files = find_files_nonrecursive(base_dir, '*.mp4')
        self.assertEqual(len(matching_files), 3)

    def test_finding_files_recursive(self):
        base_dir = tests_dir
        matching_files = find_files_recursive(base_dir, '*.mp4')
        self.assertEqual(len(matching_files), 3)

    def test_empty_path(self):
        base_dir = tests_dir
        self.assertTrue(
            check_path(
                base_dir=base_dir,
                extensions=['.mp4'],
                write_logs=False,
                method='first_audio_track',
                recursive=False,
            )
        )

    def test_full_path(self):
        base_dir = tests_dir
        self.assertFalse(
            check_path(
                base_dir=os.path.join(base_dir, 'data'),
                extensions=['.mp4'],
                write_logs=False,
                method='first_audio_track',
                recursive=False,
            )
        )

    def test_recursive_path(self):
        base_dir = tests_dir
        self.assertFalse(
            check_path(
                base_dir=base_dir,
                extensions=['.mp4'],
                write_logs=False,
                method='first_audio_track',
                recursive=True,
            )
        )

    # TODO: test main() using various CLI args


if __name__ == '__main__':
    unittest.main()
