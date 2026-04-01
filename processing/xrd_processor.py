"""
XRD PROCESSOR - Complete preprocessing pipeline
Smoothing, Baseline removal, Normalization
"""

import numpy as np
from scipy.signal import savgol_filter, medfilt
from scipy.ndimage import gaussian_filter1d

class XRDProcessor:
    """Professional XRD data processor"""
    
    def __init__(self):
        pass
    
    def smooth_savgol(self, intensity, window=11, polyorder=3):
        """
        Savitzky-Golay smoothing
        BEST for XRD - preserves peak shape
        """
        if window % 2 == 0:
            window += 1
        if window < 5:
            window = 5
        if polyorder >= window:
            polyorder = window - 2
            
        return savgol_filter(intensity, window, polyorder, mode='interp')
    
    def smooth_gaussian(self, intensity, sigma=2):
        """Gaussian smoothing - fallback method"""
        return gaussian_filter1d(intensity, sigma=sigma)
    
    def remove_baseline_minimum(self, intensity):
        """
        SIMPLE BASELINE REMOVAL
        Subtract minimum value - CRITICAL for XRD!
        """
        baseline = np.min(intensity)
        corrected = intensity - baseline
        return np.maximum(corrected, 0), baseline
    
    def remove_baseline_als(self, intensity, lam=1e5, p=0.01, niter=10):
        """
        ADVANCED BASELINE REMOVAL
        Asymmetric Least Squares (for curved baselines)
        """
        from scipy import sparse
        from scipy.sparse.linalg import spsolve
        
        L = len(intensity)
        D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L, L-2))
        w = np.ones(L)
        
        for _ in range(niter):
            W = sparse.spdiags(w, 0, L, L)
            Z = W + lam * D.dot(D.T)
            z = spsolve(Z, w * intensity)
            w = p * (intensity > z) + (1 - p) * (intensity < z)
        
        return intensity - z, z
    
    def normalize(self, intensity, method='max'):
        """
        Normalize intensity to 0-100%
        """
        if method == 'max':
            max_val = np.max(intensity)
            if max_val > 0:
                return (intensity / max_val) * 100.0
        elif method == 'area':
            area = np.trapz(intensity)
            if area > 0:
                return (intensity / area) * 100.0
        
        return intensity
    
    def full_preprocess(self, intensity, 
                       smooth_method='savgol',
                       smooth_window=11,
                       baseline_method='minimum'):
        """
        COMPLETE PREPROCESSING PIPELINE
        """
        # STEP 1: SMOOTHING
        if smooth_method == 'savgol':
            processed = self.smooth_savgol(intensity, smooth_window)
        else:
            processed = self.smooth_gaussian(intensity, smooth_window/5)
        
        # STEP 2: BASELINE REMOVAL
        if baseline_method == 'minimum':
            processed, baseline = self.remove_baseline_minimum(processed)
        else:
            processed, baseline = self.remove_baseline_als(processed)
        
        # STEP 3: NORMALIZATION
        processed = self.normalize(processed, 'max')
        
        return processed, baseline
