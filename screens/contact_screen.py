"""
Contact screen - developer contact information.
Email: smaine.chellat@gmail.com
"""

import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser


class ContactScreen(tk.Frame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, bg="#F8F9FA")
        self.app = app_controller
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#2C3E50", height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        top_row = tk.Frame(header, bg="#2C3E50")
        top_row.pack(fill=tk.X, padx=15, pady=(10, 0))
        
        tk.Button(top_row, text="← BACK", command=self.back_to_settings, bg="#E74C3C", fg="white", 
                 font=("Arial", 10, "bold"), relief=tk.RAISED, bd=2, padx=10, pady=5).pack(side=tk.LEFT)

        tk.Label(header, text="📧 CONTACT & SUPPORT", fg="white", bg="#2C3E50", font=("Arial", 20, "bold")).pack(pady=15)

        main = tk.Frame(self, bg="#F8F9FA", padx=40, pady=30)
        main.pack(fill=tk.BOTH, expand=True)

        dev_card = tk.Frame(main, bg="white", relief=tk.RAISED, bd=2, padx=30, pady=30)
        dev_card.pack(fill=tk.X, pady=20)

        tk.Label(dev_card, text="👨‍💻", font=("Arial", 48), bg="white").pack(pady=(0, 10))
        tk.Label(dev_card, text="Dr. Smaine Chellat", font=("Arial", 20, "bold"), fg="#2C3E50", bg="white").pack()
        tk.Label(dev_card, text="Lead Developer & Crystallographer", font=("Arial", 12), fg="#7F8C8D", bg="white").pack(pady=5)

        ttk.Separator(dev_card, orient="horizontal").pack(fill=tk.X, pady=20)

        contact_frame = tk.Frame(dev_card, bg="white")
        contact_frame.pack(fill=tk.X, pady=10)

        email_frame = tk.Frame(contact_frame, bg="white")
        email_frame.pack(fill=tk.X, pady=8)
        tk.Label(email_frame, text="📧", font=("Arial", 14), bg="white", width=3).pack(side=tk.LEFT)
        tk.Label(email_frame, text="Email:", font=("Arial", 12, "bold"), bg="white", width=12, anchor=tk.W).pack(side=tk.LEFT)

        email_label = tk.Label(email_frame, text="smaine.chellat@gmail.com", font=("Arial", 12, "underline"), fg="#3498DB", bg="white", cursor="hand2")
        email_label.pack(side=tk.LEFT, padx=5)
        email_label.bind("<Button-1>", lambda _e: self.copy_email())

        tk.Button(email_frame, text="Copy", command=self.copy_email, bg="#ECF0F1", fg="#2C3E50", font=("Arial", 9), relief=tk.RAISED, bd=1).pack(
            side=tk.LEFT, padx=10
        )

        aff_frame = tk.Frame(contact_frame, bg="white")
        aff_frame.pack(fill=tk.X, pady=8)
        tk.Label(aff_frame, text="🏛️", font=("Arial", 14), bg="white", width=3).pack(side=tk.LEFT)
        tk.Label(aff_frame, text="Organization:", font=("Arial", 12, "bold"), bg="white", width=12, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(aff_frame, text="University Constantine 1", font=("Arial", 12), bg="white").pack(side=tk.LEFT, padx=5)

        dept_frame = tk.Frame(contact_frame, bg="white")
        dept_frame.pack(fill=tk.X, pady=8)
        tk.Label(dept_frame, text="🔬", font=("Arial", 14), bg="white", width=3).pack(side=tk.LEFT)
        tk.Label(dept_frame, text="Department:", font=("Arial", 12, "bold"), bg="white", width=12, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(dept_frame, text="Geological Department", font=("Arial", 12), bg="white").pack(side=tk.LEFT, padx=5)

        loc_frame = tk.Frame(contact_frame, bg="white")
        loc_frame.pack(fill=tk.X, pady=8)
        tk.Label(loc_frame, text="📍", font=("Arial", 14), bg="white", width=3).pack(side=tk.LEFT)
        tk.Label(loc_frame, text="Location:", font=("Arial", 12, "bold"), bg="white", width=12, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(loc_frame, text="Ali Mendjeli, Constantine, Algeria", font=("Arial", 12), bg="white").pack(side=tk.LEFT, padx=5)

        time_frame = tk.Frame(contact_frame, bg="white")
        time_frame.pack(fill=tk.X, pady=8)
        tk.Label(time_frame, text="⏱️", font=("Arial", 14), bg="white", width=3).pack(side=tk.LEFT)
        tk.Label(time_frame, text="Response:", font=("Arial", 12, "bold"), bg="white", width=12, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(time_frame, text="Within 24-48 hours", font=("Arial", 12), bg="white").pack(side=tk.LEFT, padx=5)

        # App Information Section
        ttk.Separator(dev_card, orient="horizontal").pack(fill=tk.X, pady=20)
        
        tk.Label(dev_card, text="APPLICATION", font=("Arial", 14, "bold"), fg="#2C3E50", bg="white").pack(anchor=tk.W, pady=(10, 15))

        app_info_frame = tk.Frame(dev_card, bg="white")
        app_info_frame.pack(fill=tk.X)

        app_name_frame = tk.Frame(app_info_frame, bg="white")
        app_name_frame.pack(fill=tk.X, pady=6)
        tk.Label(app_name_frame, text="📱", font=("Arial", 12), bg="white", width=3).pack(side=tk.LEFT)
        tk.Label(app_name_frame, text="App Name:", font=("Arial", 11, "bold"), bg="white", width=15, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(app_name_frame, text="XRD-Analyzer Pro", font=("Arial", 11), bg="white").pack(side=tk.LEFT, padx=5)

        pkg_frame = tk.Frame(app_info_frame, bg="white")
        pkg_frame.pack(fill=tk.X, pady=6)
        tk.Label(pkg_frame, text="📦", font=("Arial", 12), bg="white", width=3).pack(side=tk.LEFT)
        tk.Label(pkg_frame, text="Package:", font=("Arial", 11, "bold"), bg="white", width=15, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(pkg_frame, text="com.xrdanalyzerpro.app", font=("Arial", 11), fg="#3498DB", bg="white").pack(side=tk.LEFT, padx=5)

        ttk.Separator(main, orient="horizontal").pack(fill=tk.X, pady=30)

        support_label = tk.Label(main, text="SUPPORT CHANNELS", font=("Arial", 16, "bold"), fg="#2C3E50", bg="#F8F9FA")
        support_label.pack(anchor=tk.W, pady=(0, 20))

        channels_frame = tk.Frame(main, bg="#F8F9FA")
        channels_frame.pack(fill=tk.X)

        row1 = tk.Frame(channels_frame, bg="#F8F9FA")
        row1.pack(fill=tk.X, pady=10)

        github_frame = tk.Frame(row1, bg="white", relief=tk.RAISED, bd=1, padx=20, pady=15)
        github_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(github_frame, text="🐙", font=("Arial", 24), bg="white").pack()
        tk.Label(github_frame, text="GitHub", font=("Arial", 12, "bold"), bg="white").pack()
        tk.Button(
            github_frame,
            text="Open Issues",
            command=lambda: webbrowser.open("https://github.com/smaine-chellat/xrd-analyzer/issues"),
            bg="#2C3E50",
            fg="white",
            font=("Arial", 10),
            relief=tk.RAISED,
            bd=1,
        ).pack(pady=10)

        docs_frame = tk.Frame(row1, bg="white", relief=tk.RAISED, bd=1, padx=20, pady=15)
        docs_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(docs_frame, text="📚", font=("Arial", 24), bg="white").pack()
        tk.Label(docs_frame, text="Documentation", font=("Arial", 12, "bold"), bg="white").pack()
        tk.Button(
            docs_frame,
            text="Read the Docs",
            command=lambda: webbrowser.open("https://github.com/smaine-chellat/xrd-analyzer/wiki"),
            bg="#2C3E50",
            fg="white",
            font=("Arial", 10),
            relief=tk.RAISED,
            bd=1,
        ).pack(pady=10)

        row2 = tk.Frame(channels_frame, bg="#F8F9FA")
        row2.pack(fill=tk.X, pady=10)

        linkedin_frame = tk.Frame(row2, bg="white", relief=tk.RAISED, bd=1, padx=20, pady=15)
        linkedin_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(linkedin_frame, text="🔗", font=("Arial", 24), bg="white").pack()
        tk.Label(linkedin_frame, text="LinkedIn", font=("Arial", 12, "bold"), bg="white").pack()
        tk.Button(
            linkedin_frame,
            text="Connect",
            command=lambda: webbrowser.open("https://linkedin.com/in/smaine-chellat"),
            bg="#2C3E50",
            fg="white",
            font=("Arial", 10),
            relief=tk.RAISED,
            bd=1,
        ).pack(pady=10)

        rg_frame = tk.Frame(row2, bg="white", relief=tk.RAISED, bd=1, padx=20, pady=15)
        rg_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        tk.Label(rg_frame, text="🎓", font=("Arial", 24), bg="white").pack()
        tk.Label(rg_frame, text="ResearchGate", font=("Arial", 12, "bold"), bg="white").pack()
        tk.Button(
            rg_frame,
            text="Follow",
            command=lambda: webbrowser.open("https://researchgate.net/profile/Smaine-Chellat"),
            bg="#2C3E50",
            fg="white",
            font=("Arial", 10),
            relief=tk.RAISED,
            bd=1,
        ).pack(pady=10)

        feedback_frame = tk.LabelFrame(main, text="📝 SEND FEEDBACK", bg="#F8F9FA", font=("Arial", 14, "bold"), padx=30, pady=25)
        feedback_frame.pack(fill=tk.X, pady=30)

        tk.Label(
            feedback_frame,
            text="Your feedback helps improve XRD Analyzer Pro for the entire scientific community.",
            font=("Arial", 11),
            bg="#F8F9FA",
            fg="#2C3E50",
            wraplength=600,
        ).pack(pady=10)

        tk.Button(
            feedback_frame,
            text="SEND EMAIL TO smaine.chellat@gmail.com",
            command=self.send_email,
            bg="#3498DB",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
            relief=tk.RAISED,
            bd=3,
        ).pack(pady=20)

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
        )
        back_btn.pack(fill=tk.X, pady=10)

    def back_to_settings(self):
        from screens.settings_screen import SettingsScreen

        self.app.switch_screen(SettingsScreen)

    def copy_email(self):
        self.clipboard_clear()
        self.clipboard_append("smaine.chellat@gmail.com")
        messagebox.showinfo("Copied", "Email address copied to clipboard!")

    def send_email(self):
        webbrowser.open(
            "mailto:smaine.chellat@gmail.com?subject=XRD%20Analyzer%20Pro%20-%20Feedback&body=Dear%20Dr.%20Chellat,%0A%0A"
            "I%20am%20using%20XRD%20Analyzer%20Pro%20and%20would%20like%20to%20provide%20feedback..."
        )
