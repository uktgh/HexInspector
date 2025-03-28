import tkinter as tk
import json
import os
import hashlib

from tkinter import ttk, filedialog, messagebox
from core.buffer import MemoryBuffer
from core.cache import HexCache
from ui.hex_view import HexView
from ui.info_panel import InfoPanel
from concurrent.futures import ThreadPoolExecutor

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("HexInspector")
        self.root.geometry("1400x900")
        
        self._buffer = MemoryBuffer()
        self._hex_cache = HexCache()
        self._thread_pool = ThreadPoolExecutor(max_workers=4)
        
        self.bytes_per_row = tk.IntVar(value=16)
        self.show_offset_var = tk.BooleanVar(value=True)
        self.show_ascii_var = tk.BooleanVar(value=True)
        
        self.setup_ui()
        self.create_bindings()
        self.load_settings()
        
    def setup_ui(self):
        self.create_menu()
        
        self.main_container = ttk.Frame(self.root, padding="10")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self.create_toolbar()
        self.create_main_panel()
        self.create_status_bar()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Find...", command=self.show_find_dialog, accelerator="Ctrl+F")
        edit_menu.add_command(label="Go to Offset...", command=self.show_goto_dialog, accelerator="Ctrl+G")
        
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Show Offset", variable=self.show_offset_var, command=self.update_view)
        view_menu.add_checkbutton(label="Show ASCII", variable=self.show_ascii_var, command=self.update_view)
        
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Calculate Hashes...", command=self.calculate_hashes)
        tools_menu.add_command(label="Analyze Patterns...", command=self.analyze_patterns)
        tools_menu.add_command(label="Compare Files...", command=self.compare_files)
        
    def create_toolbar(self):
        self.toolbar = ttk.Frame(self.main_container)
        self.toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(self.toolbar, text="Open", style="Accent.TButton", command=self.open_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="Save", command=self.save_file).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        search_frame = ttk.LabelFrame(self.toolbar, text="Search", padding=5)
        search_frame.pack(side=tk.LEFT, padx=10)
        
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=2)
        ttk.Button(search_frame, text="Find", style="Accent.TButton", command=self.search).pack(side=tk.LEFT, padx=2)
        
        view_frame = ttk.LabelFrame(self.toolbar, text="View Options", padding=5)
        view_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Label(view_frame, text="Bytes per row:").pack(side=tk.LEFT, padx=2)
        ttk.Spinbox(view_frame, from_=8, to=32, width=3, textvariable=self.bytes_per_row, command=self.update_view).pack(side=tk.LEFT, padx=2)
        
    def create_main_panel(self):
        self.paned_window = ttk.PanedWindow(self.main_container, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        self.hex_view = HexView(self.paned_window, self._buffer, self._hex_cache, self.bytes_per_row, self.show_offset_var, self.show_ascii_var)
        self.hex_view.pack(fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(self.paned_window)
        
        self.info_panel = InfoPanel(self.notebook)
        self.notebook.add(self.info_panel, text="Information")
        
        self.analysis_panel = InfoPanel(self.notebook)
        self.notebook.add(self.analysis_panel, text="Analysis")
        
        self.structure_panel = InfoPanel(self.notebook)
        self.notebook.add(self.structure_panel, text="Structure")
        
        self.paned_window.add(self.hex_view, weight=3)
        self.paned_window.add(self.notebook, weight=1)
        
    def create_status_bar(self):
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar()
        self.position_var = tk.StringVar()
        self.size_var = tk.StringVar()
        
        ttk.Label(self.status_frame, textvariable=self.status_var, relief=tk.SUNKEN).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(self.status_frame, textvariable=self.position_var, relief=tk.SUNKEN, width=20).pack(side=tk.LEFT)
        ttk.Label(self.status_frame, textvariable=self.size_var, relief=tk.SUNKEN, width=20).pack(side=tk.LEFT)

    def show_find_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Find")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        
        ttk.Label(dialog, text="Search for:").pack(pady=5)
        
        search_frame = ttk.Frame(dialog)
        search_frame.pack(fill=tk.X, padx=5)
        
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        options_frame = ttk.Frame(dialog)
        options_frame.pack(fill=tk.X, pady=5)
        
        self.match_case_var = tk.BooleanVar()
        self.search_hex_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Match case", variable=self.match_case_var).pack(side=tk.LEFT)
        ttk.Checkbutton(options_frame, text="Search hex", variable=self.search_hex_var).pack(side=tk.LEFT)
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Find Next", style="Accent.TButton", command=self.perform_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)

    def show_goto_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Go to Offset")
        dialog.geometry("300x120")
        dialog.transient(self.root)
        
        ttk.Label(dialog, text="Enter offset (hex):").pack(pady=5)
        
        self.offset_var = tk.StringVar()
        offset_entry = ttk.Entry(dialog, textvariable=self.offset_var)
        offset_entry.pack(fill=tk.X, padx=5)
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Go", style="Accent.TButton", command=self.goto_offset).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)

    def compare_files(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Compare Files")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        
        file_frame = ttk.LabelFrame(dialog, text="Files to Compare", padding=5)
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(file_frame, text="File 1:").grid(row=0, column=0, sticky=tk.W)
        self.file1_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file1_var).grid(row=0, column=1, sticky=tk.EW)
        ttk.Button(file_frame, text="Browse...", command=self.browse_file1).grid(row=0, column=2)
        
        ttk.Label(file_frame, text="File 2:").grid(row=1, column=0, sticky=tk.W)
        self.file2_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file2_var).grid(row=1, column=1, sticky=tk.EW)
        ttk.Button(file_frame, text="Browse...", command=self.browse_file2).grid(row=1, column=2)
        
        options_frame = ttk.LabelFrame(dialog, text="Options", padding=5)
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.ignore_case_var = tk.BooleanVar()
        self.show_differences_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Ignore case", variable=self.ignore_case_var).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Show only differences", variable=self.show_differences_var).pack(anchor=tk.W)
        
        results_frame = ttk.LabelFrame(dialog, text="Results", padding=5)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.results_text = tk.Text(results_frame, height=10)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Compare", style="Accent.TButton", command=self.compare).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=dialog.destroy).pack(side=tk.LEFT)

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.bytes_per_row.set(settings.get('bytes_per_row', 16))
        except FileNotFoundError:
            pass

    def save_settings(self):
        settings = {
            'bytes_per_row': self.bytes_per_row.get()
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as f:
                data = f.read()
                self._buffer.set_data(data)
                self.hex_view.update_view()
                self.info_panel.update_info(f"File: {file_path}\nSize: {len(data)} bytes")
                self.update_analysis_panel(data)
                self.update_structure_panel(data)
                self.status_var.set(f"Opened {file_path}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".bin")
        if file_path:
            with open(file_path, 'wb') as f:
                data = self._buffer.get_data()
                f.write(data)
                self.status_var.set(f"Saved {file_path}")

    def save_as(self):
        self.save_file()

    def show_hashes(self):
        data = self._buffer[:]
        md5 = hashlib.md5(data).hexdigest()
        sha1 = hashlib.sha1(data).hexdigest()
        sha256 = hashlib.sha256(data).hexdigest()
        hashes_info = f"MD5: {md5}\nSHA-1: {sha1}\nSHA-256: {sha256}"
        messagebox.showinfo("Hashes", hashes_info)

    def calculate_hashes(self):
        data = self._buffer[:]
        md5 = hashlib.md5(data).hexdigest()
        sha1 = hashlib.sha1(data).hexdigest()
        sha256 = hashlib.sha256(data).hexdigest()
        hashes_info = f"MD5: {md5}\nSHA-1: {sha1}\nSHA-256: {sha256}"
        messagebox.showinfo("Hashes", hashes_info)

    def analyze_patterns(self):
        data = self._buffer[:]
        pattern_info = self.find_patterns(data)
        self.show_patterns_dialog(pattern_info)

    def show_patterns_dialog(self, pattern_info):
        dialog = tk.Toplevel(self.root)
        dialog.title("Pattern Analysis")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        
        text = tk.Text(dialog, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True)
        text.insert(tk.END, pattern_info)
        text.config(state=tk.DISABLED)
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Close", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def find_patterns(self, data):
        patterns = {}
        for i in range(len(data) - 1):
            pair = bytes(data[i:i+2])
            if pair in patterns:
                patterns[pair] += 1
            else:
                patterns[pair] = 1
        sorted_patterns = sorted(patterns.items(), key=lambda item: item[1], reverse=True)
        pattern_info = "\n".join(f"{pair.hex()}: {count}" for pair, count in sorted_patterns if count > 1)
        return pattern_info

    def search(self):
        search_term = self.search_var.get()
        self.hex_view.search(search_term)

    def perform_search(self):
        search_term = self.search_entry.get()
        if not self.match_case_var.get():
            search_term = search_term.lower()
        self.hex_view.search(search_term)

    def create_bindings(self):
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-f>", lambda event: self.show_find_dialog())
        self.root.bind("<Control-g>", lambda event: self.show_goto_dialog())

    def update_view(self):
        self.hex_view.update_view()

    def goto_offset(self):
        offset = self.offset_var.get()
        if offset:
            try:
                offset = int(offset, 16)
                self.hex_view.goto_offset(offset)
            except ValueError:
                messagebox.showerror("Error", "Invalid offset value")

    def browse_file1(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file1_var.set(file_path)

    def browse_file2(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file2_var.set(file_path)

    def compare(self):
        file1_path = self.file1_var.get()
        file2_path = self.file2_var.get()
        if file1_path and file2_path:
            with open(file1_path, 'rb') as f1, open(file2_path, 'rb') as f2:
                data1 = f1.read()
                data2 = f2.read()
                differences = self.find_differences(data1, data2)
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, differences)

    def find_differences(self, data1, data2):
        differences = []
        length = min(len(data1), len(data2))
        for i in range(length):
            if data1[i] != data2[i]:
                differences.append(f"Offset {i:08X}: {data1[i]:02X} != {data2[i]:02X}")
        if len(data1) > length:
            differences.append(f"File 1 has extra data starting at offset {length:08X}")
        if len(data2) > length:
            differences.append(f"File 2 has extra data starting at offset {length:08X}")
        return "\n".join(differences)

    def update_analysis_panel(self, data):
        unique_bytes = len(set(data))
        self.analysis_panel.update_info(f"Unique bytes: {unique_bytes}\n")

    def update_structure_panel(self, data):
        hex_representation = ' '.join(f"{byte:02X}" for byte in data[:16])
        self.structure_panel.update_info(f"First 16 bytes: {hex_representation}\n")