"""
Application constants and configuration defaults.
"""

import os

APP_NAME = "XRD Analyzer Pro"
VERSION = "2.0.0"
AUTHOR = "XRD Analysis Team"
YEAR = "2026"

SUPPORTED_FORMATS = {
    "Bruker": [".xrdml", ".raw", ".lis", ".lst"],
    "PANalytical": [".rd", ".sd", ".udf", ".udi"],
    "Rigaku": [".dat", ".asc", ".uxd"],
    "General": [".txt", ".csv", ".xy", ".chi"],
    "Other": [".idf", ".fp", ".di", ".pro", ".usd", ".lhp", ".rfl", ".xy"],
}

ALL_EXTENSIONS = []
for formats in SUPPORTED_FORMATS.values():
    ALL_EXTENSIONS.extend(formats)
ALL_EXTENSIONS = list(set(ALL_EXTENSIONS))

FILE_FILTER = [
    ("All XRD Files", "*" + " *".join(ALL_EXTENSIONS)),
    ("Bruker XRDML", "*.xrdml"),
    ("Bruker RAW", "*.raw"),
    ("Bruker LIS", "*.lis"),
    ("Bruker LST", "*.lst"),
    ("PANalytical RD", "*.rd"),
    ("PANalytical SD", "*.sd"),
    ("PANalytical UDF", "*.udf"),
    ("PANalytical UDI", "*.udi"),
    ("Rigaku DAT", "*.dat"),
    ("Rigaku ASC", "*.asc"),
    ("Rigaku UXD", "*.uxd"),
    ("ASCII/Text", "*.txt *.csv *.xy *.chi"),
    ("IDF", "*.idf"),
    ("FP", "*.fp"),
    ("DI", "*.di"),
    ("PRO", "*.pro"),
    ("USD", "*.usd"),
    ("LHP", "*.lhp"),
    ("RFL", "*.rfl"),
    ("All Files", "*.*"),
]

DEFAULT_SMOOTHING_WINDOW = 7
SMOOTHING_OPTIONS = [7, 9, 11, 13, 15, 17, 19, 21]

DEFAULT_KALPHA2_RATIO = 0.5
KALPHA2_OPTIONS = [0.3, 0.4, 0.5, 0.6, 0.7]

DEFAULT_BG_GRANULARITY = 10
DEFAULT_BG_BENDING = 2
BG_GRANULARITY_OPTIONS = [5, 10, 15, 20, 25, 30]
BG_BENDING_OPTIONS = [1, 2, 3, 4, 5]

MIN_PEAK_INTENSITY = 5.0
MIN_PEAK_PROMINENCE = 2.0
MIN_PEAK_WIDTH = 3
WAVELENGTH_CU_KA = 1.5406

HOME_SCREEN_SIZE = "480x800"
GRAPH_SCREEN_SIZE = "1024x600"

PINCH_ZOOM_SENSITIVITY = 0.1
DOUBLE_TAP_THRESHOLD = 300
SWIPE_THRESHOLD = 50

CSV_HEADERS = [
    "Peak_Number",
    "Two_Theta (deg)",
    "d_spacing (Å)",
    "Intensity (counts)",
    "Intensity (%)",
    "FWHM (deg)",
    "Peak_Prominence",
    "Peak_Width (pixels)",
]

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
DATA_DIR = os.path.join(ROOT_DIR, "data")
