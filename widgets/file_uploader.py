"""File upload widget with a browse button."""

import tkinter as tk
from tkinter import filedialog


class FileUploader(tk.Frame):
    def __init__(self, parent, filetypes, on_select, **kwargs):
        super().__init__(parent, **kwargs)
        self.filetypes = filetypes
        self.on_select = on_select

        self.path_var = tk.StringVar(value="")
        entry = tk.Entry(self, textvariable=self.path_var, width=40)
        entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        browse_btn = tk.Button(self, text="Browse", command=self.browse)
        browse_btn.pack(side=tk.RIGHT, padx=5)

    def browse(self):
        filepath = filedialog.askopenfilename(title="Select XRD Data File", filetypes=self.filetypes)
        if filepath:
            self.path_var.set(filepath)
            self.on_select(filepath)
