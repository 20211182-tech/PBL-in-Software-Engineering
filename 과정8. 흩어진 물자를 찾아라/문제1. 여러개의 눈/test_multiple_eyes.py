import unittest
from pathlib import Path

from multiple_eyes import (
    CODECS,
    KEY_CTRL_C,
    KEY_CTRL_X,
    KEY_CTRL_Z,
    KEY_ESC,
    WAIT_TIME_MS,
    build_output_path,
    ensure_directory,
    is_capture_key,
    is_exit_key,
    is_record_start_key,
    is_record_stop_key,
)


class TestMultipleEyes(unittest.TestCase):
    def test_constants_match_assignment(self):
        self.assertEqual(WAIT_TIME_MS, 33)
        self.assertEqual(KEY_ESC, 27)
        self.assertEqual(KEY_CTRL_Z, 26)
        self.assertEqual(KEY_CTRL_X, 24)
        self.assertEqual(KEY_CTRL_C, 3)
        self.assertIn('mp4v', CODECS)
        self.assertIn('XVID', CODECS)

    def test_key_helpers(self):
        self.assertTrue(is_exit_key(KEY_ESC))
        self.assertTrue(is_capture_key(KEY_CTRL_Z))
        self.assertTrue(is_record_start_key(KEY_CTRL_X))
        self.assertTrue(is_record_stop_key(KEY_CTRL_C))
        self.assertFalse(is_exit_key(KEY_CTRL_C))

    def test_build_output_path_uses_timestamp_format(self):
        output_path = build_output_path(
            directory=Path('captures'),
            extension='png',
            now_text='20260514_03-10-11',
        )

        self.assertEqual(output_path, Path('captures') / '20260514_03-10-11.png')

    def test_ensure_directory_creates_nested_folder(self):
        target = Path('tmp_test_output') / 'captures'
        created_path = ensure_directory(target)

        self.assertEqual(created_path, target)
        self.assertTrue(target.exists())

        target.rmdir()
        target.parent.rmdir()


if __name__ == '__main__':
    unittest.main()
