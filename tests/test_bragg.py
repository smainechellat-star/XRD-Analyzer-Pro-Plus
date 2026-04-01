import unittest
import numpy as np

from processing.bragg_law import BraggLaw


class TestBraggLaw(unittest.TestCase):
    def test_two_theta_to_d(self):
        bragg = BraggLaw(wavelength=1.5406)
        two_theta = 30.0
        d = bragg.two_theta_to_d(two_theta)
        expected = 1.5406 / (2 * np.sin(np.radians(two_theta / 2.0)))
        self.assertAlmostEqual(float(d), float(expected), places=6)

    def test_d_to_two_theta(self):
        bragg = BraggLaw(wavelength=1.5406)
        d = 3.1355
        two_theta = bragg.d_to_two_theta(d)
        expected = 2.0 * np.degrees(np.arcsin(1.5406 / (2.0 * d)))
        self.assertAlmostEqual(float(two_theta), float(expected), places=6)


if __name__ == "__main__":
    unittest.main()
