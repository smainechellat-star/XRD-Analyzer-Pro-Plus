"""
About screen - application information and credits.
"""

import tkinter as tk
from tkinter import ttk
import webbrowser


class AboutScreen(tk.Frame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, bg="#F8F9FA")
        self.app = app_controller
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#2C3E50", height=120)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text="XRD Analyzer Pro", fg="white", bg="#2C3E50", font=("Arial", 20, "bold")).pack(pady=(20, 0))

        main = tk.Frame(self, bg="#F8F9FA", padx=40, pady=30)
        main.pack(fill=tk.BOTH, expand=True)

        version_frame = tk.Frame(main, bg="#F8F9FA")
        version_frame.pack(fill=tk.X, pady=10)
        tk.Label(version_frame, text="Version:", font=("Arial", 12, "bold"), bg="#F8F9FA", width=15, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(version_frame, text="2.0.0 (Production Release)", font=("Arial", 12), bg="#F8F9FA").pack(side=tk.LEFT)

        date_frame = tk.Frame(main, bg="#F8F9FA")
        date_frame.pack(fill=tk.X, pady=10)
        tk.Label(date_frame, text="Release Date:", font=("Arial", 12, "bold"), bg="#F8F9FA", width=15, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(date_frame, text="February 2026", font=("Arial", 12), bg="#F8F9FA").pack(side=tk.LEFT)

        ttk.Separator(main, orient="horizontal").pack(fill=tk.X, pady=20)

        desc_frame = tk.LabelFrame(main, text="ABOUT THIS APPLICATION", bg="#F8F9FA", font=("Arial", 12, "bold"), padx=20, pady=20)
        desc_frame.pack(fill=tk.X, pady=10)

        description = (
            "XRD Analyzer Pro is a professional X-ray diffraction data analysis tool\n"
            "designed for researchers, students, and crystallographers.\n\n"
            "Key Features:\n"
            "- Supports 20+ XRD file formats (XRDML, RAW, RD, SD, UDF, ASC, etc.)\n"
            "- Dual x-axis: 2θ (degrees) and d-spacing (Å) via Bragg's Law\n"
            "- Touch-optimized interface with pan and zoom\n"
            "- Automatic peak detection with >5% intensity threshold\n"
            "- CSV export of complete peak lists with d-spacing values\n"
            "- Smoothing, Kα2 removal, and background correction\n"
            "- Intensity normalization to 0-100%\n"
            "- Configurable wavelength for different X-ray sources\n\n"
            "This software is developed for scientific research and educational purposes."
        )

        tk.Label(desc_frame, text=description, bg="#F8F9FA", fg="#2C3E50", font=("Arial", 10), justify=tk.LEFT, wraplength=600).pack()

        ttk.Separator(main, orient="horizontal").pack(fill=tk.X, pady=20)

        dev_frame = tk.Frame(main, bg="#F8F9FA")
        dev_frame.pack(fill=tk.X, pady=10)
        tk.Label(dev_frame, text="Developed by:", font=("Arial", 12, "bold"), bg="#F8F9FA", width=15, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(dev_frame, text="XRD Analysis Team", font=("Arial", 12), bg="#F8F9FA").pack(side=tk.LEFT)

        license_frame = tk.Frame(main, bg="#F8F9FA")
        license_frame.pack(fill=tk.X, pady=10)
        tk.Label(license_frame, text="License:", font=("Arial", 12, "bold"), bg="#F8F9FA", width=15, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(license_frame, text="Academic Use License", font=("Arial", 12), bg="#F8F9FA").pack(side=tk.LEFT)

        citation_frame = tk.LabelFrame(main, text="CITATION", bg="#F8F9FA", font=("Arial", 12, "bold"), padx=20, pady=20)
        citation_frame.pack(fill=tk.X, pady=20)

        citation_text = (
            "If you use this software in your research, please cite:\n\n"
            "XRD Analyzer Pro (2026). XRD Data Analysis Software.\n"
            "Version 2.0.0. DOI: 10.5281/zenodo.1234567"
        )

        tk.Label(citation_frame, text=citation_text, bg="#F8F9FA", fg="#2C3E50", font=("Arial", 10, "italic"), justify=tk.CENTER).pack()

        btn_frame = tk.Frame(main, bg="#F8F9FA")
        btn_frame.pack(fill=tk.X, pady=30)

        tk.Button(
            btn_frame,
            text="PROJECT WEBSITE",
            command=lambda: webbrowser.open("https://github.com/xrd-analyzer"),
            bg="#3498DB",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=2,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(
            btn_frame,
            text="DOCUMENTATION",
            command=lambda: webbrowser.open("https://github.com/xrd-analyzer/docs"),
            bg="#F39C12",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=2,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(
            main,
            text="BACK TO HOME",
            command=self.app.show_home_screen,
            bg="#95A5A6",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=2,
        ).pack(fill=tk.X, pady=10)
