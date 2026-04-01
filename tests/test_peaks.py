import unittest
import numpy as np

from processing.peak_detection import PeakDetector


class TestPeakDetection(unittest.TestCase):
    def test_detect_peaks_basic(self):
        x = np.linspace(10, 80, 1000)
        y = (
            10 * np.exp(-((x - 20) ** 2) / (2 * 0.2 ** 2))
            + 40 * np.exp(-((x - 40) ** 2) / (2 * 0.3 ** 2))
            + 5 * np.random.default_rng(0).random(len(x))
        )

        detector = PeakDetector(min_intensity_percent=5.0, min_prominence=2.0)
        peaks = detector.detect_peaks(x, y)
        self.assertTrue(len(peaks) >= 2)


if __name__ == "__main__":
    unittest.main()
