"""
Processing screen for smoothing, Kα2 removal, and background correction.
"""

import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np
from scipy.ndimage import gaussian_filter1d


class ProcessingScreen(tk.Frame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, bg="#F8F9FA")
        self.app = app_controller
        self.data = self.app.data_manager.current_data

        if self.data is None:
            messagebox.showerror("Error", "No data loaded")
            self.app.show_home_screen()
            return

        self.setup_ui()
        self.processed_intensity = None

    def setup_ui(self):
        header = tk.Frame(self, bg="#2C3E50", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Settings button (cogwheel) in top-right corner
        btn_settings_header = tk.Button(header, text="⚙️",
                                       command=self.show_settings,
                                       bg='#34495E', fg='white',
                                       font=('Arial', 16),
                                       relief=tk.FLAT, bd=0,
                                       cursor='hand2',
                                       padx=10, pady=5)
        btn_settings_header.place(relx=1.0, rely=0.5, anchor=tk.E, x=-10)

        tk.Label(header, text="XRD DATA PROCESSING", fg="white", bg="#2C3E50", font=("Arial", 16, "bold")).pack(
            pady=20
        )

        main = tk.Frame(self, bg="#F8F9FA", padx=40, pady=30)
        main.pack(fill=tk.BOTH, expand=True)

        smooth_frame = tk.LabelFrame(
            main, text="SMOOTHING", bg="#F8F9FA", font=("Arial", 12, "bold"), padx=20, pady=15
        )
        smooth_frame.pack(fill=tk.X, pady=10)

        row1 = tk.Frame(smooth_frame, bg="#F8F9FA")
        row1.pack(fill=tk.X)

        tk.Label(row1, text="Window Size:", bg="#F8F9FA", font=("Arial", 11)).pack(side=tk.LEFT, padx=10)

        self.smooth_var = tk.IntVar(value=7)
        smooth_combo = ttk.Combobox(
            row1, textvariable=self.smooth_var, values=[7, 9, 11, 13, 15, 17, 19, 21], width=10, state="readonly"
        )
        smooth_combo.pack(side=tk.LEFT, padx=10)

        tk.Label(row1, text="(odd numbers, higher = smoother)", bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 9)).pack(
            side=tk.LEFT, padx=10
        )

        self.smooth_preview_btn = tk.Button(
            smooth_frame, text="Preview Smoothing", command=self.preview_smoothing, bg="#3498DB", fg="white", font=("Arial", 10)
        )
        self.smooth_preview_btn.pack(side=tk.RIGHT, padx=10)

        kalpha_frame = tk.LabelFrame(
            main, text="REMOVE Kα2", bg="#F8F9FA", font=("Arial", 12, "bold"), padx=20, pady=15
        )
        kalpha_frame.pack(fill=tk.X, pady=10)

        row2 = tk.Frame(kalpha_frame, bg="#F8F9FA")
        row2.pack(fill=tk.X)

        tk.Label(row2, text="Intensity Ratio:", bg="#F8F9FA", font=("Arial", 11)).pack(side=tk.LEFT, padx=10)

        self.kalpha_var = tk.DoubleVar(value=0.5)
        kalpha_combo = ttk.Combobox(
            row2, textvariable=self.kalpha_var, values=[0.3, 0.4, 0.5, 0.6, 0.7], width=10, state="readonly"
        )
        kalpha_combo.pack(side=tk.LEFT, padx=10)

        tk.Label(row2, text="(Cu Kα2/Kα1 ratio, typically 0.5)", bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 9)).pack(
            side=tk.LEFT, padx=10
        )

        self.kalpha_preview_btn = tk.Button(
            kalpha_frame,
            text="Preview Kα2 Removal",
            command=self.preview_kalpha2,
            bg="#3498DB",
            fg="white",
            font=("Arial", 10),
        )
        self.kalpha_preview_btn.pack(side=tk.RIGHT, padx=10)

        bg_frame = tk.LabelFrame(
            main, text="BACKGROUND REMOVAL", bg="#F8F9FA", font=("Arial", 12, "bold"), padx=20, pady=15
        )
        bg_frame.pack(fill=tk.X, pady=10)

        row3 = tk.Frame(bg_frame, bg="#F8F9FA")
        row3.pack(fill=tk.X)

        tk.Label(row3, text="Granularity:", bg="#F8F9FA", font=("Arial", 11)).pack(side=tk.LEFT, padx=10)

        self.bg_gran_var = tk.IntVar(value=10)
        gran_combo = ttk.Combobox(
            row3, textvariable=self.bg_gran_var, values=[5, 10, 15, 20, 25, 30], width=10, state="readonly"
        )
        gran_combo.pack(side=tk.LEFT, padx=10)

        tk.Label(row3, text="Bending:", bg="#F8F9FA", font=("Arial", 11)).pack(side=tk.LEFT, padx=20)

        self.bg_bend_var = tk.IntVar(value=2)
        bend_combo = ttk.Combobox(
            row3, textvariable=self.bg_bend_var, values=[1, 2, 3, 4, 5], width=10, state="readonly"
        )
        bend_combo.pack(side=tk.LEFT, padx=10)

        tk.Label(row3, text="(higher = more flexible)", bg="#F8F9FA", fg="#7F8C8D", font=("Arial", 9)).pack(
            side=tk.LEFT, padx=10
        )

        self.bg_preview_btn = tk.Button(
            bg_frame,
            text="Preview Background Removal",
            command=self.preview_background,
            bg="#3498DB",
            fg="white",
            font=("Arial", 10),
        )
        self.bg_preview_btn.pack(side=tk.RIGHT, padx=10)

        preview_frame = tk.LabelFrame(main, text="PREVIEW", bg="#F8F9FA", font=("Arial", 12, "bold"), padx=20, pady=15)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        self.preview_text = tk.Text(preview_frame, height=8, font=("Courier", 10), bg="white", fg="#2C3E50", relief=tk.SUNKEN, bd=2)
        self.preview_text.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.preview_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.preview_text.yview)

        self.preview_text.insert(tk.END, "Select a processing option above to preview...\n")
        self.preview_text.config(state=tk.DISABLED)

        btn_frame = tk.Frame(main, bg="#F8F9FA")
        btn_frame.pack(fill=tk.X, pady=20)

        self.apply_btn = tk.Button(
            btn_frame,
            text="APPLY ALL PROCESSING",
            command=self.apply_all,
            bg="#27AE60",
            fg="white",
            font=("Arial", 14, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=3,
        )
        self.apply_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.reset_btn = tk.Button(
            btn_frame,
            text="RESET TO RAW",
            command=self.reset_to_raw,
            bg="#E74C3C",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=3,
        )
        self.reset_btn.pack(side=tk.RIGHT, padx=5)

        back_btn = tk.Button(
            main,
            text="BACK TO HOME",
            command=self.app.show_home_screen,
            bg="#95A5A6",
            fg="white",
            font=("Arial", 11, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=2,
        )
        back_btn.pack(fill=tk.X, pady=10)

    def preview_smoothing(self):
        window = self.smooth_var.get()

        try:
            sigma = window / 5.0
            smoothed = gaussian_filter1d(self.data["intensity_raw"], sigma=sigma)

            raw_noise = np.std(self.data["intensity_raw"] - gaussian_filter1d(self.data["intensity_raw"], sigma=2))
            smooth_noise = np.std(self.data["intensity_raw"] - smoothed)
            noise_reduction = (1 - smooth_noise / raw_noise) * 100

            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, f"SMOOTHING PREVIEW (Window = {window})\n")
            self.preview_text.insert(tk.END, f"{'=' * 50}\n\n")
            self.preview_text.insert(tk.END, f"Raw noise level:      {raw_noise:.2f}\n")
            self.preview_text.insert(tk.END, f"Smoothed noise level: {smooth_noise:.2f}\n")
            self.preview_text.insert(tk.END, f"Noise reduction:      {noise_reduction:.1f}%\n\n")
            self.preview_text.insert(tk.END, "Smoothing applied. Click 'APPLY ALL' to keep changes.")
            self.preview_text.config(state=tk.DISABLED)

            self.processed_intensity = smoothed

        except Exception as exc:
            messagebox.showerror("Error", f"Smoothing failed:\n{str(exc)}")

    def preview_kalpha2(self):
        ratio = self.kalpha_var.get()

        try:
            from processing.xrd_processor import XRDProcessor

            processor = XRDProcessor()
            corrected = processor.remove_kalpha2(self.data["two_theta"], self.data["intensity_raw"], ratio)

            max_raw = np.max(self.data["intensity_raw"])
            max_corr = np.max(corrected)
            peak_reduction = (1 - max_corr / max_raw) * 100

            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, f"Kα2 REMOVAL PREVIEW (Ratio = {ratio:.3f})\n")
            self.preview_text.insert(tk.END, f"{'=' * 50}\n\n")
            self.preview_text.insert(tk.END, f"Raw peak intensity:  {max_raw:.0f} counts\n")
            self.preview_text.insert(tk.END, f"Corrected intensity: {max_corr:.0f} counts\n")
            self.preview_text.insert(tk.END, f"Peak reduction:      {peak_reduction:.1f}%\n\n")
            self.preview_text.insert(tk.END, "Kα2 removed. Click 'APPLY ALL' to keep changes.")
            self.preview_text.config(state=tk.DISABLED)

            self.processed_intensity = corrected

        except Exception as exc:
            messagebox.showerror("Error", f"Kα2 removal failed:\n{str(exc)}")

    def preview_background(self):
        granularity = self.bg_gran_var.get()
        bending = self.bg_bend_var.get()

        try:
            from processing.xrd_processor import XRDProcessor

            processor = XRDProcessor()
            corrected, background = processor.remove_background(
                self.data["two_theta"], self.data["intensity_raw"], granularity, bending
            )

            bg_percent = (np.sum(background) / np.sum(self.data["intensity_raw"])) * 100

            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, "BACKGROUND REMOVAL PREVIEW\n")
            self.preview_text.insert(tk.END, f"Granularity: {granularity}, Bending: {bending}\n")
            self.preview_text.insert(tk.END, f"{'=' * 50}\n\n")
            self.preview_text.insert(tk.END, f"Background contribution: {bg_percent:.1f}% of total\n")
            self.preview_text.insert(tk.END, "Peak/background ratio improved\n\n")
            self.preview_text.insert(tk.END, "Background removed. Click 'APPLY ALL' to keep changes.")
            self.preview_text.config(state=tk.DISABLED)

            self.processed_intensity = corrected

        except Exception as exc:
            messagebox.showerror("Error", f"Background removal failed:\n{str(exc)}")

    def apply_all(self):
        try:
            from processing.xrd_processor import XRDProcessor

            processor = XRDProcessor()

            current = self.data["intensity_raw"].copy()
            params = {}

            if hasattr(self, "smooth_var"):
                window = self.smooth_var.get()
                sigma = window / 5.0
                current = gaussian_filter1d(current, sigma=sigma)
                params["smoothing"] = window

            if hasattr(self, "kalpha_var"):
                ratio = self.kalpha_var.get()
                current = processor.remove_kalpha2(self.data["two_theta"], current, ratio)
                params["kalpha2_ratio"] = ratio

            if hasattr(self, "bg_gran_var") and hasattr(self, "bg_bend_var"):
                granularity = self.bg_gran_var.get()
                bending = self.bg_bend_var.get()
                current, _ = processor.remove_background(self.data["two_theta"], current, granularity, bending)
                params["bg_granularity"] = granularity
                params["bg_bending"] = bending

            self.data["intensity_processed"] = current

            max_int = np.max(current)
            if max_int > 0:
                self.data["intensity_normalized"] = (current / max_int) * 100.0

            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, "PROCESSING COMPLETE\n")
            self.preview_text.insert(tk.END, f"{'=' * 50}\n\n")
            self.preview_text.insert(tk.END, "Applied parameters:\n")
            for key, value in params.items():
                self.preview_text.insert(tk.END, f"  - {key}: {value}\n")
            self.preview_text.insert(tk.END, "\n")
            self.preview_text.insert(tk.END, "Data processed. Go to GRAPH to view results.")
            self.preview_text.config(state=tk.DISABLED)

            messagebox.showinfo("Success", "Processing applied successfully. Go to 'SHOW GRAPH' to view the processed data.")

        except Exception as exc:
            messagebox.showerror("Error", f"Processing failed:\n{str(exc)}")

    def reset_to_raw(self):
        if "intensity_processed" in self.data:
            del self.data["intensity_processed"]

        max_int = np.max(self.data["intensity_raw"])
        if max_int > 0:
            self.data["intensity_normalized"] = (self.data["intensity_raw"] / max_int * 100.0)

        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, "RESET TO RAW DATA\n")
        self.preview_text.insert(tk.END, f"{'=' * 50}\n\n")
        self.preview_text.insert(tk.END, "Raw data restored.\n")
        self.preview_text.insert(tk.END, "No processing applied.\n\n")
        self.preview_text.insert(tk.END, "Ready for new processing.")
        self.preview_text.config(state=tk.DISABLED)

        self.processed_intensity = None
    
    def show_settings(self):
        """Navigate to settings screen"""
        from screens.settings_screen import SettingsScreen
        self.app.switch_screen(SettingsScreen)
