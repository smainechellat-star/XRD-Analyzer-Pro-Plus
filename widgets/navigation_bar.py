"""Top navigation bar widget."""

import tkinter as tk


class NavigationBar(tk.Frame):
    def __init__(self, parent, title, on_back=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg=kwargs.get("bg", "#2C3E50"), height=60)
        self.pack_propagate(False)

        if on_back:
            tk.Button(self, text="Back", command=on_back, bg="#34495E", fg="white").pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(self, text=title, bg=kwargs.get("bg", "#2C3E50"), fg="white", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=10)
