# 📚 XRD Analyzer Pro Plus (v2.0.0)

**Advanced XRD Pattern Analysis & Mineral Identification Software**

[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.19236138-blue)](https://doi.org/10.5281/zenodo.19236138)
[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com/smainechellat/xrd-analyzer-pro)

**XRD Analyzer Pro Plus** is a free, open-source desktop application designed to democratize qualitative mineral analysis. It provides a powerful alternative to expensive commercial software, featuring a modular architecture capable of parsing over 25 XRD formats and utilizing the Crystallography Open Database (COD) for phase matching.

---

## 🚀 Quick Start Guide

1.  **📂 Load XRD File**: Click 'UPLOAD XRD FILE' on the Home screen. Supports RAW, XRDML, ASC, TXT, and more.
2.  **💾 Load Database**: Load a mineral database (SQLite `.db`/`.sqlite` or JSON `.json`).
3.  **⚙️ Process Data**: Apply smoothing, Kα2 removal, and background correction.
4.  **📈 Find Peaks**: Detect peaks automatically with adjustable thresholds.
5.  **🔬 Identify Minerals**: Run automatic phase identification using the weighted scoring algorithm.
6.  **📥 Export Results**: Save graphs, peak lists, and identification reports (Excel, CSV, PNG).

> **💡 Pro Tips:**
> *   **Double-click** on minerals in the results list to add them to the graph with color-coded peaks.
> *   **Multiple minerals** at the same peak will show comma-separated labels.
> *   Use the **mouse wheel** to zoom in/out on the graph.
> *   **R² > 0.96** indicates an excellent match (96%+ confidence).

---

## ✨ New Features in Version 2.0

*   **🎨 Multi-Mineral Overlay**: Add multiple minerals with different colors. Labels combine intelligently at shared peaks.
*   **📊 R² Correlation**: Statistical confidence score for each identification (e.g., 0.96 = 96% match quality).
*   **🔍 Dynamic Database Detection**: Automatically detects database structure; works with SQLite and JSON formats without code changes.
*   **📦 ZIP Archive Support**: Load compressed database files directly.
*   **📈 Three-Zone Identification**: View candidates, detailed info, and confidence breakdown simultaneously.
*   **📄 PDF Report Generation**: Generate professional reports with graphs and data.
*   **⚡ Batch Processing**: Process multiple XRD files efficiently.
*   **🎯 Intelligent Peak Matching**: Uses a weighted algorithm (70% d-spacing + 30% intensity) for optimal results.

---

## 📂 Supported File Formats

### XRD Data Files (25+ Formats)
| Vendor | Extensions |
| :--- | :--- |
| **Bruker** | `.xrdml`, `.raw`, `.lis`, `.lst` |
| **PANalytical** | `.sd`, `.udi` |
| **Rigaku** | `.dat`, `.asc`, `.uxd` |
| **Shimadzu** | `.raw`, `.txt` |
| **Generic/ASCII** | `.txt`, `.csv`, `.xy`, `.chi`, `.asc` |

> **⚠️ Note on Proprietary Formats:** While the software supports many formats, some legacy binary files (e.g., specific `.rd` or `.udf` versions) may require conversion to ASCII or XRDML if automatic parsing fails.

### Database Files
*   ✅ **SQLite**: `.db`, `.sqlite`, `.sqlite3`
*   ✅ **JSON**: `.json`
*   ✅ **Archives**: `.zip` (containing DB files)

---

## 🔬 Identification Algorithm

The software uses a robust weighted scoring system:

$$ \text{Confidence} = (\text{d-spacing Accuracy} \times 0.7) + (\text{Intensity Correlation} \times 0.3) $$

*   **d-spacing Accuracy**: Matches peak positions (Tolerance: ±0.02 Å).
*   **Intensity Correlation**: Matches relative peak heights.
*   **R² Score**: Coefficient of determination indicating overall fit quality.

**Match Quality Indicators:**
*   **R² ≥ 0.96**: Excellent Match ⭐⭐⭐⭐⭐
*   **R² ≥ 0.90**: Very Good Match ⭐⭐⭐⭐
*   **R² ≥ 0.80**: Good Match ⭐⭐⭐
*   **R² < 0.70**: Poor Match (Verify manually)

---

## 🛠️ Installation

### Requirements
*   Python 3.8 or higher
*   pip (Python package installer)

### Steps
1.  Clone the repository:
    ```bash
    git clone https://github.com/smainechellat/xrd-analyzer-pro.git
    cd xrd-analyzer-pro
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python main.py
    ```

---

## 📖 How to Cite

If you use XRD Analyzer Pro Plus in your research, please cite it as follows:

**APA Style:**
> Chellat, S. (2026). *XRD Analyzer Pro Plus: A Comprehensive Python-Based Software for X-ray Diffraction Pattern Analysis with Multi-Format Support and Automated Mineral Identification* (Version 2.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.19236138

**BibTeX:**
```bibtex
@software{chellat_xrd_analyzer_2026,
  author = {Chellat, Smaine},
  title = {XRD Analyzer Pro Plus: A Comprehensive Python-Based Software for X-ray Diffraction Pattern Analysis},
  year = {2026},
  publisher = {Zenodo},
  version = {2.0.0},
  doi = {10.5281/zenodo.19236138},
  url = {https://doi.org/10.5281/zenodo.19236138}
}
