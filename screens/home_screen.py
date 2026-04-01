"""
PORTRAIT HOME SCREEN - Processing parameter selection only
Process button moved to Graph Screen
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import numpy as np
from file_loader import XRDFileLoader
from dataclasses import dataclass
from typing import List, Optional, Tuple

# ===== SECONDARY PARSER SECTION =====
@dataclass
class Point:
    x: float
    y: float
    z: Optional[float] = None
    meta: Optional[dict] = None

def parse_raw(text: str) -> List[Point]:
    points = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            parts = line.split()
            x = float(parts[0])
            y = float(parts[1])
            z = float(parts[2]) if len(parts) > 2 else None
            points.append(Point(x=x, y=y, z=z))
        except (ValueError, IndexError):
            continue
    return points

def parse_rd(text: str) -> List[Point]:
    points = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            parts = line.split()
            x = float(parts[0])
            y = float(parts[1])
            z = float(parts[2]) if len(parts) > 2 else None
            points.append(Point(x=x, y=y, z=z))
        except (ValueError, IndexError):
            continue
    return points

def parse_ras(text: str) -> List[Point]:
    points = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            parts = line.split()
            x = float(parts[0])
            y = float(parts[1])
            z = float(parts[2]) if len(parts) > 2 else None
            points.append(Point(x=x, y=y, z=z))
        except (ValueError, IndexError):
            continue
    return points

def parse_udf(text: str) -> List[Point]:
    points = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            parts = line.split()
            x = float(parts[0])
            y = float(parts[1])
            z = float(parts[2]) if len(parts) > 2 else None
            points.append(Point(x=x, y=y, z=z))
        except (ValueError, IndexError):
            continue
    return points

def parse_xy(text: str) -> List[Point]:
    points = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            parts = line.split()
            x = float(parts[0])
            y = float(parts[1])
            points.append(Point(x=x, y=y))
        except (ValueError, IndexError):
            continue
    return points

def parse_section(format_name: str, text: str) -> List[Point]:
    format_name = format_name.lower().strip()
    if format_name == "raw":
        return parse_raw(text)
    if format_name == "rd":
        return parse_rd(text)
    if format_name == "ras":
        return parse_ras(text)
    if format_name == "udf":
        return parse_udf(text)
    if format_name in ["xy", "asc", "dat", "txt"]:
        return parse_xy(text)
    raise ValueError(f"Unknown format: {format_name}")

# ===== MAIN UI CLASS =====
class HomeScreen(tk.Frame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, bg='#F8F9FA')
        self.app = app_controller
        self.loader = XRDFileLoader()
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg='#2C3E50', height=100)
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
        
        tk.Label(header, text="XRD ANALYZER PRO Plus", 
                fg='white', bg='#2C3E50', 
                font=('Arial', 20, 'bold')).pack(pady=20)
        
        tk.Label(header, text="Upload & Configure Processing Parameters", 
                fg='#ECF0F1', bg='#2C3E50', 
                font=('Arial', 10)).pack()
        
        # Main content
        content = tk.Frame(self, bg='#F8F9FA', padx=30, pady=20)
        content.pack(fill=tk.BOTH, expand=True)
        
        # ===== UPLOAD SECTION =====
        upload_frame = tk.LabelFrame(content, text="📂 1. UPLOAD XRD FILE", 
                                    bg='#F8F9FA', font=('Arial', 12, 'bold'),
                                    padx=20, pady=15)
        upload_frame.pack(fill=tk.X, pady=10)
        
        self.btn_upload = tk.Button(upload_frame, 
                                   text="📂 UPLOAD XRD FILE (RAW→ASC AUTO)",
                                   command=self.upload_and_convert,
                                   bg='#3498DB', fg='white',
                                   font=('Arial', 12, 'bold'),
                                   height=2, relief=tk.RAISED, bd=3)
        self.btn_upload.pack(fill=tk.X, pady=5)
        
        # File info
        info_row = tk.Frame(upload_frame, bg='#F8F9FA')
        info_row.pack(fill=tk.X, pady=5)
        
        tk.Label(info_row, text="File:", font=('Arial', 10, 'bold'),
                bg='#F8F9FA', width=8, anchor=tk.W).pack(side=tk.LEFT)
        
        self.file_label = tk.Label(info_row, text="No file loaded",
                                  bg='white', relief=tk.SUNKEN,
                                  font=('Arial', 10), anchor=tk.W,
                                  width=40)
        self.file_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # ===== HORIZONTAL SPLIT CONTAINER (PARAMETERS + ADVICE) =====
        split_container = tk.Frame(content, bg='#F8F9FA')
        split_container.pack(fill=tk.X, pady=10)

        # --- LEFT: PROCESSING PARAMETERS ---
        params_frame = tk.LabelFrame(split_container, text="🔧 2. SELECT PROCESSING PARAMETERS", 
                                    bg='#F8F9FA', font=('Arial', 12, 'bold'),
                                    padx=15, pady=15)
        params_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # --- SMOOTHING ---
        smooth_row = tk.Frame(params_frame, bg='#F8F9FA')
        smooth_row.pack(fill=tk.X, pady=5)
        tk.Label(smooth_row, text="✓ Smoothing:", font=('Arial', 10, 'bold'),
                bg='#F8F9FA', width=12, anchor=tk.W).pack(side=tk.LEFT)
        self.smooth_var = tk.IntVar(value=7)
        smooth_combo = ttk.Combobox(smooth_row, textvariable=self.smooth_var,
                                   values=[7, 9, 11, 13, 15, 17, 19, 21],
                                   width=5, state='readonly')
        smooth_combo.pack(side=tk.LEFT, padx=5)
        
        # --- Kα2 REMOVAL ---
        kalpha_row = tk.Frame(params_frame, bg='#F8F9FA')
        kalpha_row.pack(fill=tk.X, pady=5)
        tk.Label(kalpha_row, text="✓ Remove Kα2:", font=('Arial', 10, 'bold'),
                bg='#F8F9FA', width=12, anchor=tk.W).pack(side=tk.LEFT)
        self.kalpha_var = tk.DoubleVar(value=0.5)
        kalpha_combo = ttk.Combobox(kalpha_row, textvariable=self.kalpha_var,
                                   values=[0.3, 0.4, 0.5, 0.6, 0.7],
                                   width=5, state='readonly')
        kalpha_combo.pack(side=tk.LEFT, padx=5)
        
        # --- BACKGROUND REMOVAL ---
        bg_row = tk.Frame(params_frame, bg='#F8F9FA')
        bg_row.pack(fill=tk.X, pady=5)
        tk.Label(bg_row, text="✓ Background:", font=('Arial', 10, 'bold'),
                bg='#F8F9FA', width=12, anchor=tk.W).pack(side=tk.LEFT)
        self.bg_gran_var = tk.IntVar(value=10)
        bg_gran_combo = ttk.Combobox(bg_row, textvariable=self.bg_gran_var,
                                    values=[5, 10, 15, 20, 25, 30],
                                    width=4, state='readonly')
        bg_gran_combo.pack(side=tk.LEFT, padx=2)
        tk.Label(bg_row, text=",", bg='#F8F9FA').pack(side=tk.LEFT)
        self.bg_bend_var = tk.IntVar(value=2)
        bg_bend_combo = ttk.Combobox(bg_row, textvariable=self.bg_bend_var,
                                    values=[1, 2, 3, 4, 5],
                                    width=4, state='readonly')
        bg_bend_combo.pack(side=tk.LEFT, padx=2)
        
        # --- 2θ RANGE ---
        range_row = tk.Frame(params_frame, bg='#F8F9FA')
        range_row.pack(fill=tk.X, pady=5)
        tk.Label(range_row, text="✓ 2θ Range:", font=('Arial', 10, 'bold'),
                bg='#F8F9FA', width=12, anchor=tk.W).pack(side=tk.LEFT)
        self.range_var = tk.StringVar(value="5° - 90° (Standard)")
        range_combo = ttk.Combobox(range_row, textvariable=self.range_var,
                                  values=["5° - 90°", "5° - 150°", "0° - 180°"],
                                  width=12, state='readonly')
        range_combo.pack(side=tk.LEFT, padx=5)

        # --- RIGHT: ADVICE SECTION ---
        advice_frame = tk.LabelFrame(split_container, text="Advice", 
                                    bg='#F8F9FA', font=('Arial', 12, 'bold'),
                                    padx=15, pady=15)
        advice_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        advice_text = ("The application performs well with ASC, TXT, XRDML, and DAT files. "
                      "but has moderate performance with RAW, SD, and XY formats. "
                      "Use an external converter to convert RD and RAS formats to supported formats first. ")
                      
        
        lbl_advice = tk.Label(advice_frame, text=advice_text, 
                             font=('Arial', 10), fg='#2980B9', bg='#F8F9FA',
                             wraplength=250, justify=tk.LEFT)
        lbl_advice.pack(fill=tk.BOTH, expand=True)
        
        # Info message (Below the split container)
        tk.Label(content, 
                text="ℹ️ These parameters will be applied when you click 'PROCESS DATA' in the Graph Screen",
                font=('Arial', 9, 'italic'), fg='#3498DB', bg='#F8F9FA',
                wraplength=400).pack(pady=5)
        
        # ===== ACTION BUTTONS =====
        action_frame = tk.Frame(content, bg='#F8F9FA')
        action_frame.pack(fill=tk.X, pady=10)
        
        self.btn_graph = tk.Button(action_frame,
                                  text="📊 SHOW XRD GRAPH",
                                  command=self.app.show_graph_screen,
                                  bg='#27AE60', fg='white',
                                  font=('Arial', 12, 'bold'),
                                  height=1, relief=tk.RAISED, bd=2,
                                  state=tk.DISABLED)
        self.btn_graph.pack(fill=tk.X, pady=3)
        
        self.btn_reset = tk.Button(action_frame,
                                  text="🔄 RESET ALL",
                                  command=self.reset_all,
                                  bg='#E74C3C', fg='white',
                                  font=('Arial', 10, 'bold'),
                                  height=1, relief=tk.RAISED, bd=2)
        self.btn_reset.pack(fill=tk.X, pady=3)
        
        # Status bar
        status_frame = tk.Frame(content, bg='#F8F9FA', relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(status_frame, 
                                    text="✓ Ready - Upload a file and configure parameters",
                                    bg='#F8F9FA', fg='#27AE60',
                                    font=('Arial', 10, 'bold'),
                                    padx=10, pady=5)
        self.status_label.pack(anchor=tk.W)
    
    def upload_and_convert(self):
        filepath = filedialog.askopenfilename(
            title="Select XRD File",
            filetypes=[
                ("All XRD files", "*.xrdml *.raw *.ras *.rd *.csv *.txt *.dat *.asc *.xy *.sd"),
                ("XRDML files", "*.xrdml"),
                ("Bruker RAW", "*.raw"),
                ("Rigaku RAS", "*.ras"),
                ("Rigaku RD", "*.rd"),
                ("CSV files", "*.csv"),
                ("Text files", "*.txt"),
                ("DAT files", "*.dat"),
                ("ASCII files", "*.asc *.xy *.sd"),
                ("All Files", "*.*")
            ]
        )
        
        if not filepath:
            return
        
        try:
            self.status_label.config(text="⏳ Loading file...", fg='#F39C12')
            self.update()
            
            data = self.loader.load_file(filepath)
            
            # Fallback
            if data is None:
                ext = os.path.splitext(filepath)[1][1:].lower()
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        text_content = f.read()
                    points = parse_section(ext, text_content)
                    if points:
                        data = {
                            'two_theta': [p.x for p in points],
                            'intensity_raw': [p.y for p in points],
                            'format': f"Fallback-{ext.upper()}"
                        }
                except Exception:
                    pass
            
            if data is None:
                messagebox.showerror("Error", "Could not parse file.")
                return

            self.app.data_manager.current_data = data
            self.app.data_manager.add_recent_file(filepath)
            self.app.data_manager.processing_params = {
                'smoothing': self.smooth_var.get(),
                'kalpha2_ratio': self.kalpha_var.get(),
                'bg_granularity': self.bg_gran_var.get(),
                'bg_bending': self.bg_bend_var.get()
            }
            
            self.file_label.config(text=os.path.basename(filepath))
            self.btn_graph.config(state=tk.NORMAL)
            self.status_label.config(text="✅ Loaded successfully", fg='#27AE60')
            
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)[:40]}", fg='#E74C3C')

    def show_settings(self):
        from screens.settings_screen import SettingsScreen
        self.app.switch_screen(SettingsScreen)
    
    def reset_all(self):
        if messagebox.askyesno("Reset", "Clear all data and reset?"):
            self.app.data_manager.current_data = None
            self.file_label.config(text="No file loaded")
            self.btn_graph.config(state=tk.DISABLED)
            self.smooth_var.set(11)
            self.kalpha_var.set(0.5)
            self.bg_gran_var.set(10)
            self.bg_bend_var.set(2)
            self.status_label.config(text="✓ Ready", fg='#27AE60')