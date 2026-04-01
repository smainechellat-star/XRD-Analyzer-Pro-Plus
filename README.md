# XRD-Analyzer-Pro-Plus
XRD Analyzer Pro Plus – Free, open‑source Python app for XRD mineral identification. Supports 20+ formats, weighted scoring with R² confidence, interactive graphs, multi‑file overlay, batch export. MIT license. GitHub: smainechellat/xrd-analyzer-pro
"""
README & user guide screen - complete documentation with author information.
Updated with all new features: multi-mineral overlay, R² correlation, 
dynamic database detection, batch processing, and PDF reporting.
Database support: SQLite (.db, .sqlite, .sqlite3) and JSON (.json) formats.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser


class ReadmeScreen(tk.Frame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, bg="#F8F9FA")
        self.app = app_controller
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#2C3E50", height=160)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        top_row = tk.Frame(header, bg="#2C3E50")
        top_row.pack(fill=tk.X, padx=15, pady=(10, 0))
        
        tk.Button(top_row, text="← BACK", command=self.back_to_settings, bg="#E74C3C", fg="white", 
                 font=("Arial", 10, "bold"), relief=tk.RAISED, bd=2, padx=10, pady=5).pack(side=tk.LEFT)

        # Title and badges
        tk.Label(header, text="📚 XRD ANALYZER PRO Plus v2.0", fg="white", bg="#2C3E50", 
                font=("Arial", 20, "bold")).pack(pady=5)
        tk.Label(header, text="Advanced XRD Pattern Analysis & Mineral Identification Software", 
                fg="#ECF0F1", bg="#2C3E50", font=("Arial", 12)).pack()
        
        # Badges frame
        badges_frame = tk.Frame(header, bg="#2C3E50")
        badges_frame.pack(pady=8)
        
        # DOI Badge
        doi_label = tk.Label(badges_frame, text="📄 DOI: 10.5281/zenodo.19236138", 
                bg="#2C3E50", fg="#ECF0F1", font=("Arial", 9, "bold"),
                cursor="hand2")
        doi_label.pack(side=tk.LEFT, padx=5)
        doi_label.bind("<Button-1>", lambda e: self._open_url("https://doi.org/10.5281/zenodo.19236138"))
        
        # License Badge
        license_label = tk.Label(badges_frame, text="⚖️ MIT License", 
                bg="#2C3E50", fg="#ECF0F1", font=("Arial", 9, "bold"),
                cursor="hand2")
        license_label.pack(side=tk.LEFT, padx=5)
        license_label.bind("<Button-1>", lambda e: self._open_url("https://opensource.org/licenses/MIT"))
        
        # Python Badge
        tk.Label(badges_frame, text="🐍 Python 3.8+", 
                bg="#2C3E50", fg="#ECF0F1", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Platform Badge
        tk.Label(badges_frame, text="💻 Windows | Linux | macOS", 
                bg="#2C3E50", fg="#ECF0F1", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Version Badge
        tk.Label(badges_frame, text="📦 v2.0.0", 
                bg="#2C3E50", fg="#F39C12", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)

        main = tk.Frame(self, bg="#F8F9FA", padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(main)
        notebook.pack(fill=tk.BOTH, expand=True)

        # ===== QUICK START TAB =====
        quick_tab = tk.Frame(notebook, bg="white", padx=30, pady=25)
        notebook.add(quick_tab, text="🚀 Quick Start")

        tk.Label(quick_tab, text="QUICK START GUIDE", font=("Arial", 16, "bold"), fg="#2C3E50", bg="white").pack(
            anchor=tk.W, pady=(0, 20)
        )

        steps = [
            ("1️⃣", "LOAD XRD FILE", "Click 'UPLOAD XRD FILE' on Home screen", "#3498DB"),
            ("2️⃣", "LOAD DATABASE", "Load mineral database (SQLite .db/.sqlite or JSON .json)", "#9B59B6"),
            ("3️⃣", "PROCESS DATA", "Apply smoothing, Kα2 removal, background correction", "#F39C12"),
            ("4️⃣", "FIND PEAKS", "Detect peaks with adjustable threshold", "#27AE60"),
            ("5️⃣", "IDENTIFY MINERALS", "Run automatic phase identification", "#E74C3C"),
            ("6️⃣", "EXPORT RESULTS", "Save graphs, peak lists, and identification reports", "#8E44AD"),
        ]

        for icon, title, desc, color in steps:
            row = tk.Frame(quick_tab, bg="white")
            row.pack(fill=tk.X, pady=8)
            tk.Label(row, text=icon, font=("Arial", 14, "bold"), bg="white", width=3).pack(side=tk.LEFT)
            tk.Label(row, text=title, font=("Arial", 12, "bold"), bg="white", fg=color, width=18, anchor=tk.W).pack(side=tk.LEFT, padx=10)
            tk.Label(row, text=desc, font=("Arial", 11), bg="white").pack(side=tk.LEFT, padx=20)

        tip_frame = tk.Frame(quick_tab, bg="#FFF3CD", relief=tk.RAISED, bd=1)
        tip_frame.pack(fill=tk.X, pady=30, padx=20)

        tk.Label(tip_frame, text="💡 PRO TIPS", font=("Arial", 12, "bold"), bg="#FFF3CD", fg="#856404").pack(
            anchor=tk.W, padx=15, pady=(10, 5)
        )
        tk.Label(
            tip_frame,
            text=(
                "• Double-click on minerals in Zone A to add them to the graph with color-coded peaks\n"
                "• Multiple minerals at the same peak show comma-separated labels with individual colors\n"
                "• Use mouse wheel or pinch-to-zoom for detailed analysis\n"
                "• Hover cursor over peaks to see real-time 2θ and d-spacing values\n"
                "• R² values >0.96 indicate excellent matches (96%+ confidence)"
            ),
            font=("Arial", 10),
            bg="#FFF3CD",
            fg="#856404",
            wraplength=650,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, padx=15, pady=(0, 10))

        # ===== NEW FEATURES TAB =====
        features_tab = tk.Frame(notebook, bg="white", padx=30, pady=25)
        notebook.add(features_tab, text="✨ New Features v2.0")

        tk.Label(features_tab, text="WHAT'S NEW IN VERSION 2.0", font=("Arial", 16, "bold"), fg="#2C3E50", bg="white").pack(
            anchor=tk.W, pady=(0, 20)
        )

        features = [
            ("🎨 Multi-Mineral Overlay", "Add multiple minerals with different colors. Labels combine with commas at shared peaks.", "#E74C3C"),
            ("📊 R² Correlation", "Statistical confidence score (0.96 = 96% match quality) for each identification.", "#27AE60"),
            ("🔍 Dynamic Database Detection", "Automatically detects database structure - works with SQLite and JSON formats.", "#3498DB"),
            ("📦 ZIP Archive Support", "Load compressed SQLite or JSON database files directly without manual extraction.", "#F39C12"),
            ("📈 Three-Zone Identification", "Candidates, detailed info, and confidence breakdown in one view.", "#9B59B6"),
            ("📄 PDF Report Generation", "Generate professional reports with graphs, peaks, and identification results.", "#1ABC9C"),
            ("⚡ Batch Processing", "Process multiple XRD files and generate comparative reports.", "#E67E22"),
            ("🎯 Intelligent Peak Matching", "70% d-spacing accuracy + 30% intensity correlation for optimal results.", "#34495E"),
            ("🔓 Advanced File Decoding", "Automatic decryption of proprietary formats (Bruker RAW, Rigaku RD, PANalytical SD/UDF).", "#E67E22"),
        ]

        for title, desc, color in features:
            frame = tk.Frame(features_tab, bg="white")
            frame.pack(fill=tk.X, pady=12)
            tk.Label(frame, text=title, font=("Arial", 12, "bold"), fg=color, bg="white", width=28, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(frame, text=desc, font=("Arial", 10), bg="white", wraplength=450, justify=tk.LEFT).pack(side=tk.LEFT, padx=15)

        # ===== FILE FORMATS TAB =====
        formats_tab = tk.Frame(notebook, bg="white", padx=30, pady=25)
        notebook.add(formats_tab, text="📂 File Formats")

        tk.Label(formats_tab, text="SUPPORTED XRD FILE FORMATS (25+)", font=("Arial", 16, "bold"), fg="#2C3E50", bg="white").pack(
            anchor=tk.W, pady=(0, 20)
        )

        columns_frame = tk.Frame(formats_tab, bg="white")
        columns_frame.pack(fill=tk.BOTH, expand=True)

        left_col = tk.Frame(columns_frame, bg="white")
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        formats1 = [
            ("Bruker", [".xrdml", ".raw", ".lis", ".lst"]),
            ("PANalytical", [".rd", ".sd", ".udf", ".udi"]),
            ("Rigaku", [".dat", ".asc", ".uxd", ".ras"]),
            ("Shimadzu", [".raw", ".txt"]),
        ]

        for vendor, exts in formats1:
            frame = tk.Frame(left_col, bg="white")
            frame.pack(fill=tk.X, pady=8)
            tk.Label(frame, text=vendor, font=("Arial", 11, "bold"), bg="white", width=15, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(frame, text=", ".join(exts), font=("Arial", 11), bg="white").pack(side=tk.LEFT, padx=10)

        right_col = tk.Frame(columns_frame, bg="white")
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        formats2 = [
            ("Generic", [".txt", ".csv", ".xy", ".chi"]),
            ("ASCII", [".asc", ".ascii"]),
            ("XRDML", [".xrdml"]),
            ("Archive", [".zip"]),
        ]

        for vendor, exts in formats2:
            frame = tk.Frame(right_col, bg="white")
            frame.pack(fill=tk.X, pady=8)
            tk.Label(frame, text=vendor, font=("Arial", 11, "bold"), bg="white", width=15, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(frame, text=", ".join(exts), font=("Arial", 11), bg="white").pack(side=tk.LEFT, padx=10)

        note_frame = tk.Frame(formats_tab, bg="#E8F4FD", relief=tk.RAISED, bd=1)
        note_frame.pack(fill=tk.X, pady=30)

        tk.Label(note_frame, text="📌 DATABASE FORMATS", font=("Arial", 11, "bold"), bg="#E8F4FD", fg="#0C5460").pack(
            anchor=tk.W, padx=15, pady=(10, 5)
        )
        tk.Label(
            note_frame,
            text=(
                "The application supports the following database formats:\n\n"
                "✓ SQLite Database (.db, .sqlite, .sqlite3)\n"
                "✓ JSON Database (.json)\n\n"
                "The database structure is automatically detected - no need to modify code!\n"
                "Supported database features:\n"
                "• Automatic column name detection\n"
                "• Peak column identification (d1, i1, d2, i2, etc.)\n"
                "• Mineral name, formula, and category fields detection"
            ),
            font=("Arial", 10),
            bg="#E8F4FD",
            fg="#0C5460",
            wraplength=650,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, padx=15, pady=(0, 10))

        # ===== IDENTIFICATION TAB =====
        ident_tab = tk.Frame(notebook, bg="white", padx=30, pady=25)
        notebook.add(ident_tab, text="🔬 Identification")

        tk.Label(ident_tab, text="MINERAL IDENTIFICATION SYSTEM", font=("Arial", 16, "bold"), fg="#2C3E50", bg="white").pack(
            anchor=tk.W, pady=(0, 20)
        )

        # Three Zones explanation
        zones_frame = tk.Frame(ident_tab, bg="white")
        zones_frame.pack(fill=tk.X, pady=15)

        zones = [
            ("Zone A: Candidate Minerals", "#3498DB", "Sorted by confidence score with d-space and intensity match percentages, plus R² correlation"),
            ("Zone B: Detailed Information", "#27AE60", "Formula, crystal system, space group, and matched peak positions"),
            ("Zone C: Confidence Breakdown", "#E74C3C", "R² correlation, component scores (70% d-spacing, 30% intensity), and match quality indicators"),
        ]

        for title, color, desc in zones:
            frame = tk.Frame(zones_frame, bg="white", relief=tk.GROOVE, bd=1)
            frame.pack(fill=tk.X, pady=10, padx=5)
            tk.Label(frame, text=title, font=("Arial", 12, "bold"), fg=color, bg="white").pack(anchor=tk.W, padx=10, pady=(10, 5))
            tk.Label(frame, text=desc, font=("Arial", 10), bg="white", wraplength=600, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 10))

        score_frame = tk.Frame(ident_tab, bg="white")
        score_frame.pack(fill=tk.X, pady=20)

        tk.Label(score_frame, text="📊 CONFIDENCE SCORE CALCULATION", font=("Arial", 12, "bold"), fg="#8E44AD", bg="white").pack(anchor=tk.W)
        tk.Label(
            score_frame,
            text=(
                "Confidence = (d-spacing accuracy × 0.7) + (intensity correlation × 0.3) × coverage factor\n\n"
                "• d-spacing accuracy: How well peak positions match (tolerance: ±0.02 Å)\n"
                "• intensity correlation: How well peak intensities match (normalized to 0-100%)\n"
                "• coverage factor: Percentage of peaks matched\n"
                "• R²: Coefficient of determination (0.96 = 96% variance explained)\n\n"
                "R² values indicate match quality:\n"
                "  • R² ≥ 0.96: Excellent match (96%+ confidence)\n"
                "  • R² ≥ 0.90: Very good match (90%+ confidence)\n"
                "  • R² ≥ 0.80: Good match (80%+ confidence)\n"
                "  • R² ≥ 0.70: Fair match (70%+ confidence)\n"
                "  • R² < 0.70: Poor match (<70% confidence)"
            ),
            font=("Arial", 10),
            bg="white",
            fg="#2C3E50",
            wraplength=650,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, pady=10)

        # ===== TOUCH GESTURES TAB =====
        touch_tab = tk.Frame(notebook, bg="white", padx=30, pady=25)
        notebook.add(touch_tab, text="👆 Touch Gestures")

        tk.Label(touch_tab, text="TOUCH-OPTIMIZED INTERFACE", font=("Arial", 16, "bold"), fg="#2C3E50", bg="white").pack(
            anchor=tk.W, pady=(0, 30)
        )

        gestures = [
            ("🤏 PINCH TO ZOOM", "Place two fingers on the graph and pinch together to zoom out, or spread apart to zoom in.", "#3498DB"),
            ("👆 PAN/DRAG", "Touch and drag with one finger to move the graph in any direction.", "#F39C12"),
            ("🖱️ MOUSE WHEEL ZOOM", "On desktop, use mouse wheel to zoom in/out at cursor position.", "#27AE60"),
            ("🔄 DOUBLE-CLICK MINERAL", "Double-click on any mineral in Zone A to add it to the graph with color-coded peaks.", "#E74C3C"),
            ("🔄 RESET VIEW", "Click 'RESET VIEW' button or press Ctrl+0 to return to full graph view.", "#95A5A6"),
        ]

        for title, desc, color in gestures:
            frame = tk.Frame(touch_tab, bg="white")
            frame.pack(fill=tk.X, pady=15)
            tk.Label(frame, text=title, font=("Arial", 14, "bold"), fg=color, bg="white").pack(anchor=tk.W)
            tk.Label(frame, text=desc, font=("Arial", 11), bg="white", fg="#2C3E50", wraplength=650, justify=tk.LEFT).pack(
                anchor=tk.W, pady=5
            )

        # ===== ABOUT & CITATION TAB =====
        about_tab = tk.Frame(notebook, bg="white", padx=30, pady=25)
        notebook.add(about_tab, text="📖 About & Citation")

        # Author Information
        author_frame = tk.Frame(about_tab, bg="white")
        author_frame.pack(fill=tk.X, pady=10)

        tk.Label(author_frame, text="👨‍💻 AUTHOR INFORMATION", font=("Arial", 14, "bold"), fg="#2C3E50", bg="white").pack(
            anchor=tk.W, pady=(0, 15)
        )

        # Author details table
        author_details = [
            ("Name", "Smaine Chellat"),
            ("Email", "smaine.chellat@gmail.com"),
            ("ORCID", "0000-0003-4103-0436"),
            ("Affiliation", "University Constantine 1, Geological Department, Algeria"),
            ("Research Fields", "Sedimentology • Environmental Geology • XRD/XRF Analysis"),
            ("GitHub", "https://github.com/smainechellat"),
        ]

        for label, value in author_details:
            row = tk.Frame(author_frame, bg="white")
            row.pack(fill=tk.X, pady=5)
            tk.Label(row, text=label + ":", font=("Arial", 11, "bold"), bg="white", width=15, anchor=tk.W).pack(side=tk.LEFT)
            
            if label == "ORCID":
                orcid_link = tk.Label(row, text=value, font=("Arial", 10), bg="white", fg="#3498DB", cursor="hand2")
                orcid_link.pack(side=tk.LEFT, padx=10)
                orcid_link.bind("<Button-1>", lambda e: self._open_url(f"https://orcid.org/{value}"))
            elif label == "Email":
                email_link = tk.Label(row, text=value, font=("Arial", 10), bg="white", fg="#3498DB", cursor="hand2")
                email_link.pack(side=tk.LEFT, padx=10)
                email_link.bind("<Button-1>", lambda e: self._open_email(value))
            elif label == "GitHub":
                github_link = tk.Label(row, text=value, font=("Arial", 10), bg="white", fg="#3498DB", cursor="hand2")
                github_link.pack(side=tk.LEFT, padx=10)
                github_link.bind("<Button-1>", lambda e: self._open_url(value))
            else:
                tk.Label(row, text=value, font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=10)

        # Separator
        tk.Frame(about_tab, bg="#ECF0F1", height=2).pack(fill=tk.X, pady=20)

        # Citation Section
        citation_frame = tk.Frame(about_tab, bg="white")
        citation_frame.pack(fill=tk.X, pady=10)

        tk.Label(citation_frame, text="📚 HOW TO CITE", font=("Arial", 14, "bold"), fg="#2C3E50", bg="white").pack(
            anchor=tk.W, pady=(0, 15)
        )

        citation_text = (
            "Chellat, S. (2026). XRD Analyzer Pro Plus: A Comprehensive Python-Based Software "
            "for X-ray Diffraction Pattern Analysis with Multi-Format Support and Automated "
            "Mineral Identification (Version 2.0.0) [Computer software]. Zenodo. "
            "https://doi.org/10.5281/zenodo.19236138"
        )

        citation_label = tk.Label(citation_frame, text=citation_text, font=("Arial", 10), bg="#F8F9FA", 
                                   fg="#2C3E50", wraplength=700, justify=tk.LEFT, relief=tk.SUNKEN, bd=1, padx=10, pady=10)
        citation_label.pack(anchor=tk.W, pady=5, fill=tk.X)

        # DOI Badge
        doi_frame = tk.Frame(citation_frame, bg="white")
        doi_frame.pack(anchor=tk.W, pady=15)
        
        tk.Label(doi_frame, text="📄 DOI: 10.5281/zenodo.19236138", 
                font=("Arial", 11, "bold"), bg="white", fg="#2C3E50").pack(side=tk.LEFT)
        
        copy_btn = tk.Button(doi_frame, text="📋 Copy Citation", command=self.copy_citation,
                            bg="#3498DB", fg="white", font=("Arial", 9), padx=10, cursor="hand2")
        copy_btn.pack(side=tk.LEFT, padx=20)

        # BibTeX
        bibtex_frame = tk.Frame(citation_frame, bg="white")
        bibtex_frame.pack(anchor=tk.W, pady=10)
        
        tk.Label(bibtex_frame, text="BibTeX Entry:", font=("Arial", 11, "bold"), bg="white").pack(anchor=tk.W)
        
        bibtex_text = """@software{chellat_xrd_analyzer_2026,
  author = {Chellat, Smaine},
  title = {XRD Analyzer Pro Plus: A Comprehensive Python-Based Software for X-ray Diffraction Pattern Analysis},
  year = {2026},
  publisher = {Zenodo},
  version = {2.0.0},
  doi = {10.5281/zenodo.19236138},
  url = {https://doi.org/10.5281/zenodo.19236138}
}"""
        
        bibtex_label = tk.Label(citation_frame, text=bibtex_text, font=("Courier", 9), bg="#F8F9FA", 
                                 fg="#2C3E50", wraplength=700, justify=tk.LEFT, relief=tk.SUNKEN, bd=1, padx=10, pady=10)
        bibtex_label.pack(anchor=tk.W, pady=5, fill=tk.X)
        
        copy_bibtex_btn = tk.Button(citation_frame, text="📋 Copy BibTeX", command=self.copy_bibtex,
                                   bg="#27AE60", fg="white", font=("Arial", 9), padx=10, cursor="hand2")
        copy_bibtex_btn.pack(anchor=tk.W, pady=5)

        # License Section
        license_frame = tk.Frame(about_tab, bg="white")
        license_frame.pack(fill=tk.X, pady=10)

        tk.Label(license_frame, text="⚖️ LICENSE", font=("Arial", 14, "bold"), fg="#2C3E50", bg="white").pack(
            anchor=tk.W, pady=(20, 15)
        )

        tk.Label(license_frame, text="MIT License", font=("Arial", 12, "bold"), bg="white", fg="#27AE60").pack(anchor=tk.W)
        tk.Label(license_frame, text="Copyright (c) 2026 Smaine Chellat", font=("Arial", 10), bg="white").pack(anchor=tk.W, pady=5)
        tk.Label(license_frame, 
                text="Permission is hereby granted, free of charge, to any person obtaining a copy of this software...",
                font=("Arial", 9), bg="white", fg="#7F8C8D").pack(anchor=tk.W)
        tk.Label(license_frame, 
                text="Full license text available at: https://opensource.org/licenses/MIT",
                font=("Arial", 9), bg="white", fg="#3498DB", cursor="hand2").pack(anchor=tk.W)
        license_link = tk.Label(license_frame, text="https://opensource.org/licenses/MIT", 
                                font=("Arial", 9), bg="white", fg="#3498DB", cursor="hand2")
        license_link.pack(anchor=tk.W)
        license_link.bind("<Button-1>", lambda e: self._open_url("https://opensource.org/licenses/MIT"))

        # Acknowledgements
        ack_frame = tk.Frame(about_tab, bg="white")
        ack_frame.pack(fill=tk.X, pady=10)

        tk.Label(ack_frame, text="🙏 ACKNOWLEDGEMENTS", font=("Arial", 14, "bold"), fg="#2C3E50", bg="white").pack(
            anchor=tk.W, pady=(20, 15)
        )

        tk.Label(ack_frame, text="• Crystallography Open Database (COD) for mineral reference data", 
                font=("Arial", 10), bg="white").pack(anchor=tk.W, pady=2)
        tk.Label(ack_frame, text="• scipy community for peak detection algorithms", 
                font=("Arial", 10), bg="white").pack(anchor=tk.W, pady=2)
        tk.Label(ack_frame, text="• matplotlib team for visualization tools", 
                font=("Arial", 10), bg="white").pack(anchor=tk.W, pady=2)
        tk.Label(ack_frame, text="• numpy and pandas for data processing", 
                font=("Arial", 10), bg="white").pack(anchor=tk.W, pady=2)
        tk.Label(ack_frame, text="• University Constantine 1, Algeria for institutional support", 
                font=("Arial", 10), bg="white").pack(anchor=tk.W, pady=2)
        tk.Label(ack_frame, text="• Zenodo for providing open-access repository services", 
                font=("Arial", 10), bg="white").pack(anchor=tk.W, pady=2)

        # Version History
        version_frame = tk.Frame(about_tab, bg="white")
        version_frame.pack(fill=tk.X, pady=10)

        tk.Label(version_frame, text="📜 VERSION HISTORY", font=("Arial", 14, "bold"), fg="#2C3E50", bg="white").pack(
            anchor=tk.W, pady=(20, 15)
        )

        versions = [
            ("v2.0.0 (2026)", "Multi-mineral overlay, R² correlation, dynamic database detection (SQLite/JSON), ZIP support, PDF reports, advanced file decoding"),
            ("v1.0.0 (2025)", "Initial release with basic XRD analysis and mineral identification"),
        ]

        for version, desc in versions:
            frame = tk.Frame(version_frame, bg="white")
            frame.pack(fill=tk.X, pady=5)
            tk.Label(frame, text=version, font=("Arial", 10, "bold"), bg="white", fg="#E74C3C", width=12, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(frame, text=desc, font=("Arial", 9), bg="white").pack(side=tk.LEFT, padx=10)

        # Back button
        back_btn = tk.Button(
            main,
            text="BACK TO SETTINGS",
            command=self.back_to_settings,
            bg="#95A5A6",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
        )
        back_btn.pack(fill=tk.X, pady=20)

    def _open_url(self, url):
        """Open URL in default browser"""
        webbrowser.open(url)

    def _open_email(self, email):
        """Open email client"""
        webbrowser.open(f"mailto:{email}")

    def copy_citation(self):
        """Copy citation to clipboard"""
        citation = (
            "Chellat, S. (2026). XRD Analyzer Pro Plus: A Comprehensive Python-Based Software "
            "for X-ray Diffraction Pattern Analysis with Multi-Format Support and Automated "
            "Mineral Identification (Version 2.0.0) [Computer software]. Zenodo. "
            "https://doi.org/10.5281/zenodo.19236138"
        )
        self.clipboard_clear()
        self.clipboard_append(citation)
        messagebox.showinfo("Copied", "Citation copied to clipboard!")

    def copy_bibtex(self):
        """Copy BibTeX entry to clipboard"""
        bibtex = """@software{chellat_xrd_analyzer_2026,
  author = {Chellat, Smaine},
  title = {XRD Analyzer Pro Plus: A Comprehensive Python-Based Software for X-ray Diffraction Pattern Analysis},
  year = {2026},
  publisher = {Zenodo},
  version = {2.0.0},
  doi = {10.5281/zenodo.19236138},
  url = {https://doi.org/10.5281/zenodo.19236138}
}"""
        self.clipboard_clear()
        self.clipboard_append(bibtex)
        messagebox.showinfo("Copied", "BibTeX entry copied to clipboard!")

    def back_to_settings(self):
        from screens.settings_screen import SettingsScreen
        self.app.switch_screen(SettingsScreen)
