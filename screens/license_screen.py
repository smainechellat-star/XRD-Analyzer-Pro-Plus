"""
License screen - MIT License with Copyright (C) 2026 CHELLAT Smaine.
Author: Smaine Chellat
ORCID: 0000-0003-4103-0436
Affiliation: University Constantine 1, Geological Department, Algeria
Version: 2.0.0
"""

import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser


class LicenseScreen(tk.Frame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, bg="#F8F9FA")
        self.app = app_controller
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#2C3E50", height=140)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        top_row = tk.Frame(header, bg="#2C3E50")
        top_row.pack(fill=tk.X, padx=15, pady=(10, 0))
        
        tk.Button(top_row, text="← BACK", command=self.back_to_settings, bg="#E74C3C", fg="white", 
                 font=("Arial", 10, "bold"), relief=tk.RAISED, bd=2, padx=10, pady=5).pack(side=tk.LEFT)

        tk.Label(header, text="⚖️ LICENSE & TERMS", fg="white", bg="#2C3E50", font=("Arial", 20, "bold")).pack(pady=5)
        
        # Version badge
        version_badge = tk.Frame(header, bg="#F39C12", padx=10, pady=3)
        version_badge.pack(pady=5)
        tk.Label(version_badge, text="Version 2.0.0", font=("Arial", 10, "bold"), fg="white", bg="#F39C12").pack()
        
        # Author info below title
        author_info = tk.Frame(header, bg="#2C3E50")
        author_info.pack(pady=5)
        
        tk.Label(author_info, text="Smaine Chellat", font=("Arial", 11, "bold"), fg="#ECF0F1", bg="#2C3E50").pack(side=tk.LEFT, padx=5)
        tk.Label(author_info, text="|", font=("Arial", 11), fg="#ECF0F1", bg="#2C3E50").pack(side=tk.LEFT)
        
        orcid_link = tk.Label(author_info, text="ORCID: 0000-0003-4103-0436", font=("Arial", 10), fg="#3498DB", bg="#2C3E50", cursor="hand2")
        orcid_link.pack(side=tk.LEFT, padx=5)
        orcid_link.bind("<Button-1>", lambda e: self._open_url("https://orcid.org/0000-0003-4103-0436"))
        
        tk.Label(author_info, text="|", font=("Arial", 11), fg="#ECF0F1", bg="#2C3E50").pack(side=tk.LEFT)
        
        tk.Label(author_info, text="University Constantine 1, Algeria", font=("Arial", 10), fg="#ECF0F1", bg="#2C3E50").pack(side=tk.LEFT, padx=5)

        main = tk.Frame(self, bg="#F8F9FA", padx=30, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        # Create notebook for tabs
        notebook = ttk.Notebook(main)
        notebook.pack(fill=tk.BOTH, expand=True)

        # ===== LICENSE TAB =====
        license_tab = tk.Frame(notebook, bg="white", padx=20, pady=20)
        notebook.add(license_tab, text="📜 MIT License")

        license_card = tk.Frame(license_tab, bg="white", relief=tk.RAISED, bd=2, padx=25, pady=25)
        license_card.pack(fill=tk.BOTH, expand=True)

        # Copyright section with complete author details
        copyright_frame = tk.Frame(license_card, bg="#2C3E50", padx=20, pady=20)
        copyright_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(copyright_frame, text="© 2026 CHELLAT Smaine", font=("Arial", 20, "bold"), fg="white", bg="#2C3E50").pack()
        tk.Label(copyright_frame, text="XRD Analyzer Pro Plus", font=("Arial", 14), fg="#ECF0F1", bg="#2C3E50").pack(pady=5)
        
        # Additional author metadata
        author_meta = tk.Frame(copyright_frame, bg="#2C3E50")
        author_meta.pack(pady=10)
        
        email_link = tk.Label(author_meta, text="📧 smaine.chellat@gmail.com", font=("Arial", 9), fg="#ECF0F1", bg="#2C3E50", cursor="hand2")
        email_link.pack(side=tk.LEFT, padx=10)
        email_link.bind("<Button-1>", lambda e: self._open_email("smaine.chellat@gmail.com"))
        
        tk.Label(author_meta, text="🔬 Sedimentology • Environmental Geology • XRD/XRF Analysis", font=("Arial", 9), fg="#ECF0F1", bg="#2C3E50").pack(side=tk.LEFT, padx=10)

        badge_frame = tk.Frame(license_card, bg="#27AE60", padx=15, pady=8)
        badge_frame.pack(pady=10)
        tk.Label(badge_frame, text="📜 MIT LICENSE", font=("Arial", 12, "bold"), fg="white", bg="#27AE60").pack()

        ttk.Separator(license_card, orient="horizontal").pack(fill=tk.X, pady=20)

        license_text = (
            "MIT License\n\n"
            "Copyright (c) 2026 CHELLAT Smaine\n"
            "University Constantine 1, Geological Department, Algeria\n"
            "ORCID: 0000-0003-4103-0436\n\n"
            "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
            "of this software and associated documentation files (the \"Software\"), to deal\n"
            "in the Software without restriction, including without limitation the rights\n"
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
            "copies of the Software, and to permit persons to whom the Software is\n"
            "furnished to do so, subject to the following conditions:\n\n"
            "The above copyright notice and this permission notice shall be included in all\n"
            "copies or substantial portions of the Software.\n\n"
            "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
            "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
            "SOFTWARE."
        )

        text_frame = tk.Frame(license_card, bg="white")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Courier", 10),
            bg="#F8F9FA",
            fg="#2C3E50",
            relief=tk.SUNKEN,
            bd=1,
            height=18,
            padx=20,
            pady=20,
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)

        text_widget.insert(tk.END, license_text)
        text_widget.config(state=tk.DISABLED)

        # ===== THIRD-PARTY LICENSES TAB =====
        third_party_tab = tk.Frame(notebook, bg="white", padx=20, pady=20)
        notebook.add(third_party_tab, text="📚 Third-Party Licenses")

        third_party_frame = tk.Frame(third_party_tab, bg="white", relief=tk.RAISED, bd=2, padx=25, pady=25)
        third_party_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(third_party_frame, text="THIRD-PARTY SOFTWARE LICENSES", font=("Arial", 16, "bold"), fg="#2C3E50", bg="white").pack(anchor=tk.W, pady=(0, 20))

        third_party_licenses = [
            ("NumPy", "BSD 3-Clause License", "https://numpy.org/doc/stable/license.html"),
            ("SciPy", "BSD 3-Clause License", "https://www.scipy.org/scipylib/license.html"),
            ("Matplotlib", "BSD-compatible License", "https://matplotlib.org/stable/users/license.html"),
            ("Pandas", "BSD 3-Clause License", "https://pandas.pydata.org/docs/about.html#license"),
            ("Tkinter", "Python Software Foundation License", "https://docs.python.org/3/license.html"),
        ]

        for lib, license_type, url in third_party_licenses:
            frame = tk.Frame(third_party_frame, bg="white", relief=tk.GROOVE, bd=1)
            frame.pack(fill=tk.X, pady=8, padx=5)
            
            lib_label = tk.Label(frame, text=lib, font=("Arial", 11, "bold"), bg="white", fg="#3498DB")
            lib_label.pack(anchor=tk.W, padx=10, pady=(8, 2))
            
            license_label = tk.Label(frame, text=f"License: {license_type}", font=("Arial", 9), bg="white", fg="#2C3E50")
            license_label.pack(anchor=tk.W, padx=10, pady=2)
            
            url_link = tk.Label(frame, text=f"🔗 {url}", font=("Arial", 8), bg="white", fg="#27AE60", cursor="hand2")
            url_link.pack(anchor=tk.W, padx=10, pady=(2, 8))
            url_link.bind("<Button-1>", lambda e, u=url: self._open_url(u))

        # ===== CITATION TAB =====
        citation_tab = tk.Frame(notebook, bg="white", padx=20, pady=20)
        notebook.add(citation_tab, text="📖 How to Cite")

        citation_frame = tk.Frame(citation_tab, bg="white", relief=tk.RAISED, bd=2, padx=25, pady=25)
        citation_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(citation_frame, text="HOW TO CITE THIS SOFTWARE", font=("Arial", 16, "bold"), fg="#2C3E50", bg="white").pack(anchor=tk.W, pady=(0, 20))

        citation_text = (
            "Chellat, S. (2026). XRD Analyzer Pro Plus: A Comprehensive Python-Based Software "
            "for X-ray Diffraction Pattern Analysis with Multi-Format Support and Automated "
            "Mineral Identification (Version 2.0.0) [Computer software]. Zenodo. "
            "https://doi.org/10.5281/zenodo.19236138"
        )

        citation_label = tk.Label(citation_frame, text=citation_text, font=("Arial", 10), bg="#F8F9FA", 
                                   fg="#2C3E50", wraplength=650, justify=tk.LEFT, relief=tk.SUNKEN, bd=1, padx=15, pady=15)
        citation_label.pack(anchor=tk.W, pady=10, fill=tk.X)

        # BibTeX
        tk.Label(citation_frame, text="BibTeX Entry:", font=("Arial", 11, "bold"), bg="white", fg="#2C3E50").pack(anchor=tk.W, pady=(15, 5))
        
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
                                 fg="#2C3E50", wraplength=650, justify=tk.LEFT, relief=tk.SUNKEN, bd=1, padx=15, pady=15)
        bibtex_label.pack(anchor=tk.W, pady=5, fill=tk.X)

        btn_frame_cite = tk.Frame(citation_frame, bg="white")
        btn_frame_cite.pack(pady=10)
        
        copy_cite_btn = tk.Button(btn_frame_cite, text="📋 Copy Citation", command=self.copy_citation,
                                  bg="#3498DB", fg="white", font=("Arial", 10), padx=15, cursor="hand2")
        copy_cite_btn.pack(side=tk.LEFT, padx=5)
        
        copy_bibtex_btn = tk.Button(btn_frame_cite, text="📋 Copy BibTeX", command=self.copy_bibtex,
                                    bg="#27AE60", fg="white", font=("Arial", 10), padx=15, cursor="hand2")
        copy_bibtex_btn.pack(side=tk.LEFT, padx=5)

        # ===== ACCEPT SECTION =====
        accept_frame = tk.Frame(main, bg="white", pady=20)
        accept_frame.pack(fill=tk.X)

        self.accept_var = tk.BooleanVar(value=False)
        accept_check = tk.Checkbutton(
            accept_frame,
            text="I have read and accept the terms of this license and all third-party licenses",
            variable=self.accept_var,
            bg="white",
            fg="#2C3E50",
            font=("Arial", 10, "bold"),
        )
        accept_check.pack()

        btn_frame = tk.Frame(main, bg="white")
        btn_frame.pack(fill=tk.X, pady=10)

        self.accept_btn = tk.Button(
            btn_frame,
            text="✅ ACCEPT LICENSE & CONTINUE",
            command=self.accept_license,
            bg="#27AE60",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=2,
            state=tk.DISABLED,
        )
        self.accept_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        def toggle_accept_button():
            if self.accept_var.get():
                self.accept_btn.config(state=tk.NORMAL)
            else:
                self.accept_btn.config(state=tk.DISABLED)

        accept_check.config(command=toggle_accept_button)

        decline_btn = tk.Button(
            btn_frame,
            text="❌ DECLINE & EXIT",
            command=self.decline_license,
            bg="#E74C3C",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=2,
        )
        decline_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        back_btn = tk.Button(
            btn_frame,
            text="← BACK TO SETTINGS",
            command=self.back_to_settings,
            bg="#95A5A6",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=2,
        )
        back_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Info frame with DOI and contact
        info_frame = tk.Frame(main, bg="#E8F4FD", relief=tk.RAISED, bd=1, padx=15, pady=15)
        info_frame.pack(fill=tk.X, pady=10)

        tk.Label(info_frame, text="ℹ️ ABOUT THIS LICENSE", font=("Arial", 11, "bold"), bg="#E8F4FD", fg="#0C5460").pack(anchor=tk.W)
        tk.Label(
            info_frame,
            text=(
                "This software is released under the MIT License, one of the most permissive open-source licenses. "
                "You are free to use, modify, and distribute this software for academic, commercial, or personal purposes, "
                "provided that the original copyright notice is retained.\n\n"
                "📄 DOI: 10.5281/zenodo.19236138\n"
                "📧 Contact: smaine.chellat@gmail.com\n"
                "🔗 ORCID: https://orcid.org/0000-0003-4103-0436\n"
                "🐙 GitHub: https://github.com/smainechellat\n"
                "📚 Zenodo: https://zenodo.org/record/19236138"
            ),
            font=("Arial", 9),
            bg="#E8F4FD",
            fg="#0C5460",
            wraplength=650,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, pady=5)

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

    def accept_license(self):
        messagebox.showinfo(
            "License Accepted",
            "Thank you for accepting the MIT License.\n\n"
            "You may now use XRD Analyzer Pro Plus v2.0.0 freely in accordance with the terms.\n\n"
            "© 2026 CHELLAT Smaine - University Constantine 1, Algeria\n"
            "ORCID: 0000-0003-4103-0436\n"
            "DOI: 10.5281/zenodo.19236138\n\n"
            "If you use this software in your research, please cite it using the provided citation.\n\n"
            "All rights reserved under MIT License.",
        )
        self.app.show_home_screen()

    def decline_license(self):
        if messagebox.askyesno(
            "Decline License",
            "You have declined the license terms.\n\n"
            "You cannot use this software without accepting the license.\n"
            "Do you want to exit the application?",
        ):
            self.app.on_closing()

    def back_to_settings(self):
        from screens.settings_screen import SettingsScreen
        self.app.switch_screen(SettingsScreen)