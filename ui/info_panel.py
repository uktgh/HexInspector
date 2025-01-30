import tkinter as tk
from tkinter import ttk

class InfoPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.text = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED)
        self.text.pack(fill=tk.BOTH, expand=True)

    def update_info(self, info):
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, info)
        self.text.config(state=tk.DISABLED)