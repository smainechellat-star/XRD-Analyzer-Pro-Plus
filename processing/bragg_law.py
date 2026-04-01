"""
BRAGG'S LAW - Robust d-spacing Calculator
"""

import numpy as np


class BraggLaw:
    """Robust Bragg's Law calculator for XRD"""

    def __init__(self, wavelength=1.5406):
        # Cu Kα default wavelength
        self.wavelength = float(wavelength)

    def two_theta_to_d(self, two_theta):
        """
        Convert 2θ (degrees) → d-spacing (Å)
        d = λ / (2 sin θ)
        """

        two_theta = np.asarray(two_theta, dtype=float)

        theta = two_theta / 2.0
        theta_rad = np.radians(theta)

        sin_theta = np.sin(theta_rad)

        # invalid values → nan
        invalid = np.abs(sin_theta) < 1e-12

        d = np.full_like(sin_theta, np.nan)
        d[~invalid] = self.wavelength / (2.0 * sin_theta[~invalid])

        return d

    def d_to_two_theta(self, d_spacing):
        """
        Convert d-spacing (Å) → 2θ (degrees)
        """

        d_spacing = np.asarray(d_spacing, dtype=float)

        valid = d_spacing > 0

        two_theta = np.full_like(d_spacing, np.nan)

        argument = np.zeros_like(d_spacing)
        argument[valid] = self.wavelength / (2.0 * d_spacing[valid])

        argument = np.clip(argument, -1.0, 1.0)

        theta = np.degrees(np.arcsin(argument))

        two_theta[valid] = 2.0 * theta[valid]

        return two_theta
