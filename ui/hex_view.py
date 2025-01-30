import tkinter as tk
from tkinter import ttk
from core.buffer import MemoryBuffer
from core.cache import HexCache

class HexView(ttk.Frame):
    def __init__(self, parent, buffer: MemoryBuffer, cache: HexCache):
        super().__init__(parent)
        self.buffer = buffer
        self.cache = cache
        self.setup_ui()

    def setup_ui(self):
        self.text = tk.Text(self, font=("Courier", 12), wrap=tk.NONE, bg="#2e2e2e", fg="#d3d3d3", insertbackground="#d3d3d3")
        self.vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.text.xview)
        self.text.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        
        self.text.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ew")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_view(self):
        self.text.delete(1.0, tk.END)
        bytes_per_row = 16
        hex_data = self.buffer[:].hex()
        ascii_data = self.buffer[:].tobytes().decode('ascii', errors='replace')
        for i in range(0, len(hex_data), bytes_per_row * 2):
            hex_chunk = ' '.join(hex_data[j:j+2] for j in range(i, i + bytes_per_row * 2, 2))
            ascii_chunk = ''.join(c if 32 <= ord(c) < 127 else '.' for c in ascii_data[i//2:i//2 + bytes_per_row])
            self.text.insert(tk.END, f"{i//2:08X}  {hex_chunk:<{bytes_per_row*3}}  {ascii_chunk}\n")

    def goto_offset(self, offset):
        line = offset // 16 + 1
        self.text.see(f"{line}.0")
        self.text.mark_set("insert", f"{line}.0")
        self.text.focus()