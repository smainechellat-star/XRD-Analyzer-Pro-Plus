import os
import tempfile
import unittest

import numpy as np

from processing.file_parsers import UniversalXRDReader


class TestParsers(unittest.TestCase):
    def test_ascii_parser(self):
        content = "10 100\n11 150\n12 200\n"
        with tempfile.TemporaryDirectory() as temp_dir:
            path = os.path.join(temp_dir, "sample.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            data = UniversalXRDReader.parse_file(path)
            self.assertIn("two_theta", data)
            self.assertIn("intensity_raw", data)
            self.assertEqual(len(data["two_theta"]), 3)
            self.assertTrue(np.allclose(data["intensity_raw"], np.array([100, 150, 200])))


if __name__ == "__main__":
    unittest.main()
