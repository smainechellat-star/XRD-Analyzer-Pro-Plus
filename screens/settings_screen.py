"""
Settings screen for application configuration.
ENHANCED VERSION - With peak threshold and display limit settings
FINAL CORRECTED VERSION
"""

import json
import tkinter as tk
from tkinter import messagebox, ttk


class SettingsScreen(tk.Frame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, bg="#F8F9FA")
        self.app = app_controller
        self.config_path = "config.json"
        self.load_config()
        self.setup_ui()

    def load_config(self):
        """Load configuration from file, or create default if not exists"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
            
            # Ensure all required sections exist (for backward compatibility)
            self._ensure_config_structure()
                
        except FileNotFoundError:
            # Config file doesn't exist - create default
            self.config = self._get_default_config()
            self._save_config_quietly()  # Save default config for next time
        except Exception as e:
            # Other error - show warning and use defaults
            messagebox.showwarning(
                "Config Warning", 
                f"Could not load config file:\n{str(e)}\n\nUsing default settings."
            )
            self.config = self._get_default_config()

    def _ensure_config_structure(self):
        """Ensure all required sections exist in loaded config"""
        default = self._get_default_config()
        
        # Add missing top-level sections
        for key in default:
            if key not in self.config:
                self.config[key] = default[key]
        
        # Ensure nested structures exist
        if "peak_detection" in default and "peak_detection" in self.config:
            for key in default["peak_detection"]:
                if key not in self.config["peak_detection"]:
                    self.config["peak_detection"][key] = default["peak_detection"][key]
        
        if "processing" in default and "processing" in self.config:
            for key in default["processing"]:
                if key not in self.config["processing"]:
                    self.config["processing"][key] = default["processing"][key]
        
        if "gui" in default and "gui" in self.config:
            for key in default["gui"]:
                if key not in self.config["gui"]:
                    self.config["gui"][key] = default["gui"][key]
        
        if "display" in default and "display" in self.config:
            for key in default["display"]:
                if key not in self.config["display"]:
                    self.config["display"][key] = default["display"][key]

    def _get_default_config(self):
        """Return complete default configuration dictionary"""
        return {
            "app_name": "XRD Analyzer Pro",
            "version": "2.0.0",
            "author": "Smaine Chellat",
            "description": "Complete XRD Analysis Suite",
            
            "xrd_parameters": {
                "wavelength": 1.5406,
                "wavelength_nm": 0.15406,
                "wavelength_angstrom": 1.5406,
                "radiation": "Cu Kα",
                "radiation_alternatives": ["Co Kα", "Mo Kα", "Fe Kα"],
                "default_2theta_range": [5.0, 150.0],
                "default_intensity_range": [0, 100],
                "d_spacing_calculation": "bragg_law",
                "angle_unit": "degrees_2theta"
            },
            
            "peak_detection": {
                "min_intensity_percent": 5.0,
                "min_prominence": 2.0,
                "min_width": 3,
                "max_peaks": 100,
                "baseline_correction": True,
                "smoothing_before_detection": True,
                "methods": ["scipy_find_peaks", "derivative", "wavelet"]
            },
            
            "processing": {
                "smoothing_window": 7,
                "smoothing_options": [5, 7, 9, 11, 13, 15, 17, 19, 21],
                "smoothing_method": "savitzky_golay",
                "kalpha2_correction": True,
                "kalpha2_ratio": 0.5,
                "kalpha2_options": [0.3, 0.4, 0.5, 0.6, 0.7],
                "background_subtraction": {
                    "enabled": True,
                    "method": "polynomial",
                    "granularity": 10,
                    "bending": 2,
                    "order": 3
                },
                "normalization": {
                    "enabled": False,
                    "method": "max_intensity",
                    "options": ["max_intensity", "area", "com"]
                }
            },
            
            "file_formats": {
                "Bruker": [".xrdml", ".raw", ".lis", ".lst"],
                "PANalytical": [".rd", ".sd", ".udf", ".udi", ".xrdml"],
                "Rigaku": [".dat", ".asc", ".uxd", ".ras"],
                "Philips": [".rd", ".sd", ".udi", ".xrdml"],
                "Shimadzu": [".raw", ".txt"],
                "Generic": [".txt", ".csv", ".xy", ".chi", ".dat", ".asc"],
                "Other": [".idf", ".fp", ".di", ".pro", ".usd", ".lhp", ".rfl", ".gsa"]
            },
            
            "file_handling": {
                "encoding": "utf-8",
                "fallback_encodings": ["latin-1", "cp1252", "iso-8859-1"],
                "delimiter_detection": True,
                "header_skip_lines": 0,
                "column_mapping": {
                    "two_theta": ["2theta", "2_theta", "2θ", "angle", "x"],
                    "intensity": ["intensity", "counts", "y", "cps"],
                    "d_spacing": ["d_spacing", "d-spacing", "d", "d(A)"]
                },
                "auto_scale_intensity": True,
                "preserve_metadata": True
            },
            
            "export": {
                "csv": {
                    "delimiter": ",",
                    "decimal": ".",
                    "include_header": True,
                    "columns": ["2theta", "d_spacing", "intensity", "peak_label"]
                },
                "image": {
                    "format": "png",
                    "dpi": 300,
                    "formats_available": ["png", "pdf", "svg", "jpg", "tif"],
                    "transparent_bg": False
                },
                "report": {
                    "include_plot": True,
                    "include_parameters": True,
                    "include_peak_table": True,
                    "format": "pdf"
                }
            },
            
            "database": {
                "enabled": True,
                "default_source": "COD",
                "sources": ["COD", "ICDD_PDF4", "MinCryst", "AMCSD"],
                "tolerance_angstrom": 0.02,
                "max_matches_per_peak": 5,
                "min_match_confidence": 0.7,
                "cache_results": True,
                "offline_mode": False
            },
            
            "gui": {
                "home_size": "1200x700",
                "graph_size": "1400x800",
                "min_window_size": [800, 600],
                "max_window_size": [1920, 1080],
                "theme": "light",
                "themes_available": ["light", "dark", "high_contrast"],
                "font_size": 10,
                "touch_enabled": True,
                "touch_gesture_sensitivity": 0.8,
                "show_grid": True,
                "show_cursor_readout": True,
                "auto_save_session": True,
                "session_autosave_interval_minutes": 5
            },
            
            "display": {
                "peak_display_limit": 0,
                "mineral_display_limit": 0,
                "intensity_threshold": 0,
                "show_grid": True,
                "show_references": True
            },
            
            "paths": {
                "data_folder": "data",
                "assets_folder": "assets",
                "config_file": "config.json",
                "log_folder": "logs",
                "export_folder": "exports",
                "database_folder": "database",
                "temp_folder": "temp",
                "use_sys_meipass_for_bundled": True
            },
            
            "logging": {
                "enabled": True,
                "level": "INFO",
                "levels_available": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                "file_logging": True,
                "console_logging": False,
                "log_rotation": {
                    "enabled": True,
                    "max_bytes_mb": 10,
                    "backup_count": 3
                },
                "include_timestamp": True,
                "include_module": True
            },
            
            "performance": {
                "max_file_size_mb": 100,
                "cache_loaded_patterns": True,
                "cache_size_mb": 200,
                "multithread_processing": True,
                "max_threads": 4,
                "gpu_acceleration": False
            },
            
            "updates": {
                "check_for_updates": True,
                "update_channel": "stable",
                "channels_available": ["stable", "beta", "dev"],
                "auto_download": False,
                "notify_only": True
            },
            
            "advanced": {
                "debug_mode": False,
                "show_console_diagnostics": True,
                "enable_experimental_features": False,
                "custom_python_path": None,
                "external_tools": {
                    "highscore_plus_path": None,
                    "jade_path": None,
                    "fullprof_path": None
                }
            }
        }

    def _save_config_quietly(self):
        """Save config without showing error messages"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except:
            pass  # Silently fail - will try again on explicit save

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to save settings:\n{str(exc)}")
            return False

    def setup_ui(self):
        header = tk.Frame(self, bg="#2C3E50", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text="APPLICATION SETTINGS", fg="white", bg="#2C3E50", 
                font=("Arial", 16, "bold")).pack(pady=20)

        main = tk.Frame(self, bg="#F8F9FA", padx=30, pady=20)
        main.pack(fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(main)
        notebook.pack(fill=tk.BOTH, expand=True)

        # ===== XRD Parameters Tab =====
        xrd_tab = tk.Frame(notebook, bg="#F8F9FA", padx=20, pady=20)
        notebook.add(xrd_tab, text="XRD Parameters")

        # Access xrd_parameters section
        xrd_params = self.config.get("xrd_parameters", self.config)  # Fallback to old structure
        
        row = 0
        tk.Label(xrd_tab, text="X-ray Wavelength (Å):", bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )

        # Try to get wavelength from new structure, fallback to old
        wavelength_value = xrd_params.get("wavelength_angstrom", 
                           xrd_params.get("wavelength", 1.5406))
        self.wavelength_var = tk.DoubleVar(value=wavelength_value)
        tk.Entry(xrd_tab, textvariable=self.wavelength_var, width=10, 
                font=("Arial", 11)).grid(row=row, column=1, padx=20, pady=10)

        tk.Label(xrd_tab, text="(Cu Kα = 1.5406, Co Kα = 1.7903)", 
                bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 9)).grid(
            row=row, column=2, padx=10
        )
        row += 1

        tk.Label(xrd_tab, text="Radiation Source:", bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )

        radiation_value = xrd_params.get("radiation", "Cu Kα")
        self.radiation_var = tk.StringVar(value=radiation_value)
        radiation_combo = ttk.Combobox(
            xrd_tab, textvariable=self.radiation_var, 
            values=["Cu Kα", "Co Kα", "Fe Kα", "Cr Kα", "Mo Kα"], 
            width=15, state="readonly"
        )
        radiation_combo.grid(row=row, column=1, padx=20, pady=10)

        def update_wavelength(*_args):
            radiation = self.radiation_var.get()
            wavelengths = {"Cu Kα": 1.5406, "Co Kα": 1.7903, "Fe Kα": 1.9374, 
                          "Cr Kα": 2.2910, "Mo Kα": 0.7107}
            if radiation in wavelengths:
                self.wavelength_var.set(wavelengths[radiation])

        self.radiation_var.trace("w", update_wavelength)
        row += 2

        ttk.Separator(xrd_tab, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky=tk.EW, pady=20
        )
        row += 1

        tk.Label(xrd_tab, text="Default 2θ Range (degrees):", 
                bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )

        range_frame = tk.Frame(xrd_tab, bg="#F8F9FA")
        range_frame.grid(row=row, column=1, padx=20, pady=10)

        # Get 2θ range from config
        theta_range = xrd_params.get("default_2theta_range", [5, 150])
        self.two_theta_min = tk.DoubleVar(value=theta_range[0])
        self.two_theta_max = tk.DoubleVar(value=theta_range[1])

        tk.Entry(range_frame, textvariable=self.two_theta_min, width=8, 
                font=("Arial", 11)).pack(side=tk.LEFT)
        tk.Label(range_frame, text="to", bg="#F8F9FA", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        tk.Entry(range_frame, textvariable=self.two_theta_max, width=8, 
                font=("Arial", 11)).pack(side=tk.LEFT)
        row += 1

        # ===== Peak Detection Tab =====
        peak_tab = tk.Frame(notebook, bg="#F8F9FA", padx=20, pady=20)
        notebook.add(peak_tab, text="Peak Detection")

        peak_detection = self.config.get("peak_detection", {})

        row = 0
        tk.Label(peak_tab, text="Minimum Intensity (%):", bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )

        self.min_intensity_var = tk.DoubleVar(value=peak_detection.get("min_intensity_percent", 5.0))
        tk.Scale(
            peak_tab, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.min_intensity_var, 
            length=200, tickinterval=5, bg="#F8F9FA"
        ).grid(row=row, column=1, padx=20, pady=10)

        tk.Label(peak_tab, textvariable=self.min_intensity_var, bg="white", relief=tk.SUNKEN, 
                width=5, font=("Arial", 11, "bold")).grid(row=row, column=2)
        row += 1

        tk.Label(peak_tab, text="Minimum Prominence:", bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )

        self.prominence_var = tk.DoubleVar(value=peak_detection.get("min_prominence", 2.0))
        tk.Scale(
            peak_tab, from_=0.5, to=5.0, resolution=0.5, orient=tk.HORIZONTAL, 
            variable=self.prominence_var, length=200, tickinterval=1, bg="#F8F9FA"
        ).grid(row=row, column=1, padx=20, pady=10)

        tk.Label(peak_tab, textvariable=self.prominence_var, bg="white", relief=tk.SUNKEN, 
                width=5, font=("Arial", 11, "bold")).grid(row=row, column=2)
        row += 1

        tk.Label(peak_tab, text="Minimum Peak Width:", bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )

        self.width_var = tk.IntVar(value=peak_detection.get("min_width", 3))
        ttk.Combobox(peak_tab, textvariable=self.width_var, 
                    values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
                    width=10, state="readonly").grid(
            row=row, column=1, padx=20, pady=10, sticky=tk.W
        )
        row += 1

        # ===== Display Options Tab =====
        display_tab = tk.Frame(notebook, bg="#F8F9FA", padx=20, pady=20)
        notebook.add(display_tab, text="Display Options")

        gui = self.config.get("gui", {})
        display = self.config.get("display", {})

        row = 0
        
        # Theme
        tk.Label(display_tab, text="Theme:", bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )

        self.theme_var = tk.StringVar(value=gui.get("theme", "light"))
        ttk.Combobox(display_tab, textvariable=self.theme_var, 
                    values=["light", "dark", "blue"], 
                    width=15, state="readonly").grid(
            row=row, column=1, padx=20, pady=10, sticky=tk.W
        )
        row += 1

        # Touch gestures
        self.touch_var = tk.BooleanVar(value=gui.get("touch_enabled", True))
        tk.Checkbutton(display_tab, text="Enable Touch Gestures (pinch-zoom, pan)", 
                      variable=self.touch_var, bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=10
        )
        row += 2
        
        ttk.Separator(display_tab, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky=tk.EW, pady=10
        )
        row += 1
        
        # Peak Display Settings
        tk.Label(display_tab, text="PEAK DISPLAY SETTINGS", bg="#F8F9FA", fg="#2C3E50", 
                font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=(10,5)
        )
        row += 1
        
        # Grid toggle
        show_grid = display.get("show_grid", gui.get("show_grid", True))
        self.show_grid_var = tk.BooleanVar(value=show_grid)
        tk.Checkbutton(display_tab, text="Show Grid on Graph", 
                      variable=self.show_grid_var, bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=5
        )
        row += 1
        
        # Reference lines toggle
        self.show_ref_var = tk.BooleanVar(value=display.get("show_references", True))
        tk.Checkbutton(display_tab, text="Show Reference Lines (Quartz/Calcite)", 
                      variable=self.show_ref_var, bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=5
        )
        row += 1
        
        # Intensity threshold
        tk.Label(display_tab, text="Intensity Threshold:", bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )
        
        self.threshold_var = tk.IntVar(value=display.get("intensity_threshold", 0))
        threshold_combo = ttk.Combobox(display_tab, textvariable=self.threshold_var, 
                                       values=[0, 5, 25, 50, 75], width=10, state="readonly")
        threshold_combo.grid(row=row, column=1, padx=20, pady=10, sticky=tk.W)
        tk.Label(display_tab, text="% (0 = show all)", bg="#F8F9FA", fg="#7F8C8D", 
                font=("Arial", 9)).grid(row=row, column=2, padx=5)
        row += 1
        
        # Peak display limit
        tk.Label(display_tab, text="Max Peaks to Show:", bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )
        
        self.peak_limit_var = tk.IntVar(value=display.get("peak_display_limit", 0))
        peak_limit_spin = tk.Spinbox(display_tab, from_=0, to=500, 
                                     textvariable=self.peak_limit_var, width=10)
        peak_limit_spin.grid(row=row, column=1, padx=20, pady=10, sticky=tk.W)
        tk.Label(display_tab, text="(0 = show all)", bg="#F8F9FA", fg="#7F8C8D", 
                font=("Arial", 9)).grid(row=row, column=2, padx=5)
        row += 1
        
        # Mineral display limit
        tk.Label(display_tab, text="Max Minerals to Show:", bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )
        
        self.mineral_limit_var = tk.IntVar(value=display.get("mineral_display_limit", 0))
        mineral_limit_spin = tk.Spinbox(display_tab, from_=0, to=500, 
                                        textvariable=self.mineral_limit_var, width=10)
        mineral_limit_spin.grid(row=row, column=1, padx=20, pady=10, sticky=tk.W)
        tk.Label(display_tab, text="(0 = show all)", bg="#F8F9FA", fg="#7F8C8D", 
                font=("Arial", 9)).grid(row=row, column=2, padx=5)
        row += 1

        # ===== Processing Tab =====
        proc_tab = tk.Frame(notebook, bg="#F8F9FA", padx=20, pady=20)
        notebook.add(proc_tab, text="Processing")

        processing = self.config.get("processing", {})

        row = 0
        tk.Label(proc_tab, text="Default Smoothing Window:", bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )

        self.smooth_default_var = tk.IntVar(value=processing.get("smoothing_window", 7))
        ttk.Combobox(proc_tab, textvariable=self.smooth_default_var, 
                    values=[7, 9, 11, 13, 15, 17, 19, 21], width=10, state="readonly").grid(
            row=row, column=1, padx=20, pady=10, sticky=tk.W
        )
        row += 1

        tk.Label(proc_tab, text="Default Kα2 Ratio:", bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )

        self.kalpha_default_var = tk.DoubleVar(value=processing.get("kalpha2_ratio", 0.5))
        ttk.Combobox(proc_tab, textvariable=self.kalpha_default_var, 
                    values=[0.3, 0.4, 0.5, 0.6, 0.7], width=10, state="readonly").grid(
            row=row, column=1, padx=20, pady=10, sticky=tk.W
        )
        row += 1

        tk.Label(proc_tab, text="Default Background:", bg="#F8F9FA", font=("Arial", 11)).grid(
            row=row, column=0, sticky=tk.W, pady=10
        )

        bg_frame = tk.Frame(proc_tab, bg="#F8F9FA")
        bg_frame.grid(row=row, column=1, padx=20, pady=10, sticky=tk.W)

        # Try to get from nested structure, fallback to flat
        bg_subtraction = processing.get("background_subtraction", {})
        self.bg_gran_default_var = tk.IntVar(
            value=bg_subtraction.get("granularity", processing.get("bg_granularity", 10))
        )
        self.bg_bend_default_var = tk.IntVar(
            value=bg_subtraction.get("bending", processing.get("bg_bending", 2))
        )

        tk.Label(bg_frame, text="Granularity:", bg="#F8F9FA", font=("Arial", 10)).pack(side=tk.LEFT)
        ttk.Combobox(bg_frame, textvariable=self.bg_gran_default_var, 
                    values=[5, 10, 15, 20, 25, 30], width=5, state="readonly").pack(
            side=tk.LEFT, padx=5
        )

        tk.Label(bg_frame, text="Bending:", bg="#F8F9FA", font=("Arial", 10)).pack(
            side=tk.LEFT, padx=(20, 0)
        )
        ttk.Combobox(bg_frame, textvariable=self.bg_bend_default_var, 
                    values=[1, 2, 3, 4, 5], width=5, state="readonly").pack(
            side=tk.LEFT, padx=5
        )

        # ===== Help & Info Tab =====
        help_tab = tk.Frame(notebook, bg="#F8F9FA", padx=20, pady=20)
        notebook.add(help_tab, text="Help & Info")

        tk.Label(help_tab, text="DOCUMENTATION & SUPPORT", bg="#F8F9FA", fg="#2C3E50", 
                font=("Arial", 13, "bold")).pack(anchor=tk.W, pady=(0, 15))

        help_list = tk.Frame(help_tab, bg="#F8F9FA")
        help_list.pack(fill=tk.X)

        tk.Button(
            help_list,
            text="📚 README / USER GUIDE",
            command=self.show_readme_screen,
            bg="#3498DB",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=2,
        ).pack(fill=tk.X, pady=6)

        tk.Button(
            help_list,
            text="📧 CONTACT & SUPPORT",
            command=self.show_contact_screen,
            bg="#2C3E50",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=2,
        ).pack(fill=tk.X, pady=6)

        tk.Button(
            help_list,
            text="⚖️ LICENSE & TERMS",
            command=self.show_license_screen,
            bg="#27AE60",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=2,
        ).pack(fill=tk.X, pady=6)

        # ===== Buttons =====
        btn_frame = tk.Frame(main, bg="#F8F9FA")
        btn_frame.pack(fill=tk.X, pady=20)

        tk.Button(
            btn_frame,
            text="SAVE SETTINGS",
            command=self.save_settings,
            bg="#27AE60",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=3,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(
            btn_frame,
            text="RESET TO DEFAULTS",
            command=self.reset_defaults,
            bg="#E74C3C",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=3,
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

    def save_settings(self):
        """Save all settings including new display options"""
        # XRD Parameters - handle both new and old structure
        if "xrd_parameters" in self.config:
            # New structure
            self.config["xrd_parameters"]["wavelength_angstrom"] = self.wavelength_var.get()
            self.config["xrd_parameters"]["wavelength"] = self.wavelength_var.get()
            self.config["xrd_parameters"]["wavelength_nm"] = self.wavelength_var.get() * 0.1
            self.config["xrd_parameters"]["radiation"] = self.radiation_var.get()
            self.config["xrd_parameters"]["default_2theta_range"] = [
                self.two_theta_min.get(), self.two_theta_max.get()
            ]
        else:
            # Old structure (for backward compatibility)
            self.config["wavelength"] = self.wavelength_var.get()
            self.config["radiation"] = self.radiation_var.get()
            self.config["default_2theta_range"] = [
                self.two_theta_min.get(), self.two_theta_max.get()
            ]

        # Peak Detection
        if "peak_detection" in self.config:
            self.config["peak_detection"]["min_intensity_percent"] = self.min_intensity_var.get()
            self.config["peak_detection"]["min_prominence"] = self.prominence_var.get()
            self.config["peak_detection"]["min_width"] = self.width_var.get()

        # Processing
        if "processing" in self.config:
            self.config["processing"]["smoothing_window"] = self.smooth_default_var.get()
            self.config["processing"]["kalpha2_ratio"] = self.kalpha_default_var.get()
            
            # Handle nested background subtraction
            if "background_subtraction" in self.config["processing"]:
                self.config["processing"]["background_subtraction"]["granularity"] = self.bg_gran_default_var.get()
                self.config["processing"]["background_subtraction"]["bending"] = self.bg_bend_default_var.get()
            else:
                self.config["processing"]["bg_granularity"] = self.bg_gran_default_var.get()
                self.config["processing"]["bg_bending"] = self.bg_bend_default_var.get()

        # GUI
        if "gui" in self.config:
            self.config["gui"]["theme"] = self.theme_var.get()
            self.config["gui"]["touch_enabled"] = self.touch_var.get()
            self.config["gui"]["show_grid"] = self.show_grid_var.get()

        # Display settings
        if "display" in self.config:
            self.config["display"]["peak_display_limit"] = self.peak_limit_var.get()
            self.config["display"]["mineral_display_limit"] = self.mineral_limit_var.get()
            self.config["display"]["intensity_threshold"] = self.threshold_var.get()
            self.config["display"]["show_grid"] = self.show_grid_var.get()
            self.config["display"]["show_references"] = self.show_ref_var.get()

        if self.save_config():
            messagebox.showinfo("Success", 
                "Settings saved successfully.\n\n"
                "Note: Some changes may require restarting the application to take full effect.")

    def show_readme_screen(self):
        from screens.readme_screen import ReadmeScreen
        self.app.switch_screen(ReadmeScreen)

    def show_contact_screen(self):
        from screens.contact_screen import ContactScreen
        self.app.switch_screen(ContactScreen)

    def show_license_screen(self):
        from screens.license_screen import LicenseScreen
        self.app.switch_screen(LicenseScreen)

    def reset_defaults(self):
        if messagebox.askyesno("Reset", "Reset all settings to defaults?"):
            self.config = self._get_default_config()
            self.save_config()
            messagebox.showinfo("Reset", "Settings reset to defaults. Please restart the application.")
            self.app.show_home_screen()