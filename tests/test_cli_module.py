import unittest
import tempfile
import os
from os import path
from argparse import Namespace

TESTS_DIRECTORY_NAME = path.dirname(path.abspath(__file__))


class TestPathParsing(unittest.TestCase):
    _tmp_dir = None
    _initial_cwd = None

    @classmethod
    def setUpClass(cls):
        """Set up environment for the test case"""
        # Create temporary working directory for the test case
        cls._tmp_dir = tempfile.TemporaryDirectory(dir=TESTS_DIRECTORY_NAME)
        assert path.isdir(cls._tmp_dir.name)

        # Set current working directory to the new temporary directory
        cls._initial_cwd = os.getcwd()
        os.chdir(cls._tmp_dir.name)

        # Create fixture directories and files
        cls.dirs = ['dir_1', 'dir_2']
        for d in cls.dirs:
            os.mkdir(d)
            assert path.isdir(d)

        cls.files = ['file_1', 'file_2.txt']
        for f in cls.files:
            with open(f, 'w'):
                pass
            assert path.isfile(f)

        # The import is done here with the purpose of initializing parser with
        # proper working directory value
        # (it is used as default path value of parser).
        from cli import parser
        cls.parser = parser

    @classmethod
    def tearDownClass(cls):
        cls._tmp_dir.cleanup()
        os.chdir(cls._initial_cwd)

        assert not path.exists(cls._tmp_dir.name)

    def test_current_dir_by_default(self):
        """
        Test that default value of positional `path` argument is the current
        working directory.
        """
        self.assertEqual(
            self.parser.parse_args([]),
            Namespace(path={'dirs': [os.getcwd()], 'files': []}),
            "If `path` argument is omitted the default value should be the "
            "current working directory."
        )

    def test_do_not_omit_existed_paths(self):
        """
        Test that all provided `path` argument's values are accurately parsed
        if they exists are present at the file system.
        """
        self.assertEqual(
            self.parser.parse_args(self.files + self.dirs),
            Namespace(path={'dirs': self.dirs, 'files': self.files})
        )

    def test_omit_not_existed_paths(self):
        """
        Test that, all listed but not existed directory's and file's are
        filtered by the parser.
        """
        absent_files, absent_dirs = [], []
        # Get original names of non-existed directories
        # and files with `tempfile` library.
        for i in range(2):
            with tempfile.NamedTemporaryFile(
                    dir=self._tmp_dir.name) as tmp_file_obj:
                absent_files.append(tmp_file_obj.name)
            # Ensure that noting with such a name is exists on the file system.
            assert not path.exists(tmp_file_obj.name)

            with tempfile.TemporaryDirectory(
                    dir=self._tmp_dir.name) as tmp_dir_name:
                absent_dirs.append(tmp_dir_name)
            assert not path.exists(tmp_dir_name)

        self.assertEqual(
            self.parser.parse_args(absent_files + self.files + absent_dirs +
                                   self.dirs),
            Namespace(path={'dirs': self.dirs, 'files': self.files})
        )
