import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from hexviewer import HexViewer
from compression import CompressionHandler
from utils import get_file_metadata
import re

class HexInspectorGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("900x650")
        self.master.configure(bg="#2E2E2E")  # Dark Mode Background

        # Menu
        self.menubar = tk.Menu(self.master, bg="#1E1E1E", fg="white")
        
        # File Menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0, bg="#333333", fg="white")
        self.file_menu.add_command(label="Apri", command=self.open_file)
        self.file_menu.add_command(label="Salva", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Esci", command=self.master.quit)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        
        # View Menu
        self.view_menu = tk.Menu(self.menubar, tearoff=0, bg="#333333", fg="white")
        self.view_menu.add_command(label="Visualizza Metadati", command=self.show_metadata)
        self.view_menu.add_command(label="Calcola Checksum", command=self.calculate_checksum)
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Visualizza Hex", command=self.view_hex)
        self.view_menu.add_command(label="Zoom In", command=self.zoom_in)
        self.view_menu.add_command(label="Zoom Out", command=self.zoom_out)
        self.menubar.add_cascade(label="Visualizza", menu=self.view_menu)
        
        # Analyze Menu
        self.analyze_menu = tk.Menu(self.menubar, tearoff=0, bg="#333333", fg="white")
        self.analyze_menu.add_command(label="Trova Stringhe ASCII", command=self.find_ascii_strings)
        self.analyze_menu.add_command(label="Trova Header", command=self.find_headers)
        self.analyze_menu.add_separator()
        self.analyze_menu.add_command(label="Cerca Pattern Esadecimale", command=self.search_hex_pattern)
        self.analyze_menu.add_command(label="Verifica Integrità", command=self.check_integrity)
        self.analyze_menu.add_command(label="Analizza Compressione", command=self.analyze_compression)
        self.menubar.add_cascade(label="Analizza", menu=self.analyze_menu)

        self.master.config(menu=self.menubar)

        # Text Area for Hex Display
        self.text_area = tk.Text(self.master, wrap="none", height=30, width=120, bg="#1E1E1E", fg="white", font=("Courier", 10))
        self.text_area.pack(pady=20)

        # File Path
        self.filepath = None
        self.hex_viewer = None

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if filepath:
            self.filepath = filepath
            self.text_area.delete(1.0, tk.END)
            self.hex_viewer = HexViewer(filepath)
            self.view_hex()

    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filepath:
            with open(filepath, "w") as f:
                f.write(self.text_area.get(1.0, tk.END))

    def view_hex(self):
        if self.hex_viewer:
            hex_data = self.hex_viewer.get_colored_hex_data()
            # Remove ANSI escape sequences
            hex_data = self.remove_ansi_escape_sequences(hex_data)

            # Insert the clean hex data into the text widget
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, hex_data)
    
    def remove_ansi_escape_sequences(self, text):
        # Remove any ANSI color codes
        return re.sub(r'\x1b\[[0-9;]*m', '', text)

    def show_metadata(self):
        if self.filepath:
            metadata = get_file_metadata(self.filepath)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Metadata:\n{metadata}")

    def calculate_checksum(self):
        if self.filepath:
            checksum_type = simpledialog.askstring("Checksum", "Scegli il tipo (MD5, SHA1, SHA256):")
            checksum = self.hex_viewer.calculate_checksum(checksum_type)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Checksum ({checksum_type}): {checksum}")

    def zoom_in(self):
        # Estrai la dimensione del font attuale come stringa (es. "Courier 10")
        current_font = self.text_area.cget("font")
        font_name, current_font_size = current_font.split()
        
        # Converti la dimensione del font in intero
        current_font_size = int(current_font_size)
        
        # Incrementa la dimensione del font
        new_font_size = current_font_size + 2
        self.text_area.config(font=(font_name, new_font_size))

    def zoom_out(self):
        # Estrai la dimensione del font attuale come stringa (es. "Courier 10")
        current_font = self.text_area.cget("font")
        font_name, current_font_size = current_font.split()
        
        # Converti la dimensione del font in intero
        current_font_size = int(current_font_size)
        
        # Decrementa la dimensione del font, ma non scendere sotto 8
        new_font_size = max(8, current_font_size - 2)
        self.text_area.config(font=(font_name, new_font_size))

    def find_ascii_strings(self):
        if self.hex_viewer:
            ascii_strings = self.hex_viewer.find_ascii_strings()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Stringhe ASCII trovate:\n{ascii_strings}")

    def find_headers(self):
        if self.hex_viewer:
            headers = self.hex_viewer.find_headers()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Header trovati:\n{headers}")

    def search_hex_pattern(self):
        pattern = simpledialog.askstring("Pattern", "Inserisci il pattern esadecimale da cercare (es. 68 65 6C 6C 6F):")
        if self.hex_viewer:
            results = self.hex_viewer.search_pattern(pattern)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Pattern trovato:\n{results}")

    def check_integrity(self):
        if self.hex_viewer:
            integrity = self.hex_viewer.check_integrity()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Integrità del file:\n{integrity}")

    def analyze_compression(self):
        if self.hex_viewer:
            compression_info = self.hex_viewer.analyze_compression()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Analisi della compressione:\n{compression_info}")
