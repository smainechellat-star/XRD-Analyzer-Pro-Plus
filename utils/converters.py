"""
XRD Conversion Utilities
"""

import numpy as np
from processing.bragg_law import BraggLaw


class XRDConverter:
    """High-level XRD parameter converter"""

    def __init__(self, wavelength=1.5406):
        self.bragg = BraggLaw(wavelength)

    def two_theta_to_d(self, two_theta):
        """Convert 2θ angle to d-spacing in Angstroms"""
        return self.bragg.two_theta_to_d(two_theta)

    def d_to_two_theta(self, d_spacing):
        """Convert d-spacing to 2θ angle in degrees"""
        return self.bragg.d_to_two_theta(d_spacing)
    
    # ===== ADD THESE ADDITIONAL CONVERSION METHODS =====
    
    def two_theta_to_q(self, two_theta):
        """Convert 2θ angle to scattering vector Q (Å⁻¹)"""
        # Q = 4π sin(θ) / λ
        theta = np.radians(two_theta / 2.0)
        return 4 * np.pi * np.sin(theta) / self.bragg.wavelength
    
    def q_to_two_theta(self, q):
        """Convert scattering vector Q (Å⁻¹) to 2θ angle in degrees"""
        # sin(θ) = Qλ / 4π
        sin_theta = q * self.bragg.wavelength / (4 * np.pi)
        sin_theta = np.clip(sin_theta, -1, 1)  # Avoid numerical errors
        theta = np.degrees(np.arcsin(sin_theta))
        return 2 * theta
    
    def d_to_q(self, d_spacing):
        """Convert d-spacing to scattering vector Q (Å⁻¹)"""
        # Q = 2π / d
        return 2 * np.pi / d_spacing
    
    def q_to_d(self, q):
        """Convert scattering vector Q (Å⁻¹) to d-spacing (Å)"""
        # d = 2π / Q
        return 2 * np.pi / q
    
    def energy_to_wavelength(self, energy_keV):
        """Convert photon energy (keV) to wavelength (Å)"""
        # E (keV) = 12.3984 / λ (Å)
        return 12.3984 / energy_keV
    
    def wavelength_to_energy(self, wavelength):
        """Convert wavelength (Å) to photon energy (keV)"""
        # E (keV) = 12.3984 / λ (Å)
        return 12.3984 / wavelength


# ===== ADD THIS IF YOU NEED UNIT CONVERSIONS BETWEEN DIFFERENT UNITS =====
class UnitConverter:
    """Handle conversions between different XRD units"""
    
    @staticmethod
    def convert(value, from_unit, to_unit):
        """
        Convert between different units
        Supported units: 'deg' (degrees), 'rad' (radians), 'A' (Angstroms), 
                        'nm' (nanometers), 'pm' (picometers), 'q' (Å⁻¹)
        """
        # First convert to standard units
        if from_unit == to_unit:
            return value
        
        # Angle conversions
        if from_unit == 'deg' and to_unit == 'rad':
            return np.radians(value)
        elif from_unit == 'rad' and to_unit == 'deg':
            return np.degrees(value)
        
        # Length conversions
        elif from_unit == 'A' and to_unit == 'nm':
            return value * 0.1
        elif from_unit == 'nm' and to_unit == 'A':
            return value * 10
        elif from_unit == 'A' and to_unit == 'pm':
            return value * 100
        elif from_unit == 'pm' and to_unit == 'A':
            return value * 0.01
        
        # Special XRD conversions
        elif from_unit == 'deg' and to_unit == 'q':
            # Convert 2θ to Q using wavelength from converter
            # This requires wavelength to be provided separately
            raise ValueError("deg to q conversion requires wavelength - use XRDConverter.two_theta_to_q() instead")
        
        else:
            raise ValueError(f"Conversion from {from_unit} to {to_unit} not supported")