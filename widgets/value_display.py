"""Three-box cursor display widget."""

import tkinter as tk


class ValueDisplay(tk.Frame):
    def __init__(self, parent, labels=("2θ", "d", "I%"), **kwargs):
        super().__init__(parent, **kwargs)
        self.vars = []
        for label in labels:
            row = tk.Frame(self, bg=kwargs.get("bg", "#F8F9FA"))
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=f"{label}:", width=8, anchor=tk.W, bg=kwargs.get("bg", "#F8F9FA"), font=("Arial", 9, "bold")).pack(
                side=tk.LEFT
            )
            var = tk.StringVar(value="--")
            tk.Label(row, textvariable=var, bg="white", relief=tk.SUNKEN, width=12, font=("Courier", 9, "bold")).pack(side=tk.RIGHT)
            self.vars.append(var)

    def set_values(self, values):
        for var, value in zip(self.vars, values):
            var.set(value)
