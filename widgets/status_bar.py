"""Bottom status bar widget."""

import tkinter as tk


class StatusBar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg=kwargs.get("bg", "#F8F9FA"))
        self.label = tk.Label(self, text="Ready", bg=kwargs.get("bg", "#F8F9FA"), fg="#2C3E50", anchor=tk.W)
        self.label.pack(fill=tk.X, padx=8, pady=4)

    def set_text(self, text, fg="#2C3E50"):
        self.label.config(text=text, fg=fg)
