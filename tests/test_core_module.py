import unittest
import sys
import io

from core import main


class TestMainModule(unittest.TestCase):
    def setUp(self):
        self._stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        sys.stdout.close()
        sys.stdout = self._stdout

    def test_main_function(self):
        self.assertEqual(sys.stdout.getvalue(), '')

        main()

        self.assertEqual(sys.stdout.getvalue(), 'test\n')


if __name__ == '__main__':
    unittest.main()
