import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from src.hex_inspector import hex_inspector
from src.file_utils import open_compressed_file, save_file
from src.hashing import calculate_checksum
from src.ascii_logo import print_logo
import threading

def load_file_in_background(file_path, callback):
    def worker():
        try:
            hex_data = hex_inspector(file_path)
            callback(hex_data)
        except Exception as e:
            callback(str(e))
    
    thread = threading.Thread(target=worker)
    thread.start()

def open_file():
    file_path = filedialog.askopenfilename(title="Seleziona un file", filetypes=[("Tutti i file", "*.*")])
    if file_path:
        if file_path.endswith(('.zip', '.tar.gz', '.gz')):
            file_path = open_compressed_file(file_path)
        load_file_in_background(file_path, update_text_box)

def update_text_box(hex_data):
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, hex_data)

def show_checksum():
    file_path = filedialog.askopenfilename(title="Seleziona un file")
    if file_path:
        checksum = calculate_checksum(file_path, algorithm='sha256')
        messagebox.showinfo("Checksum", f"SHA256: {checksum}")

def save_file_ui():
    file_path = filedialog.asksaveasfilename(title="Salva file", filetypes=[("Tutti i file", "*.*")])
    if file_path:
        data = text_box.get(1.0, tk.END).encode('utf-8')
        save_file(file_path, data)
        messagebox.showinfo("Salvato", f"File salvato in {file_path}")

def create_ui():
    global text_box, root
    root = tk.Tk()
    root.title("HexInspector v0.3.0")
    root.geometry("800x600")

    print_logo()  # Stampa il logo ASCII

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Apri", command=open_file)
    file_menu.add_command(label="Salva", command=save_file_ui)
    file_menu.add_command(label="Checksum", command=show_checksum)
    file_menu.add_separator()
    file_menu.add_command(label="Esci", command=root.quit)

    label = tk.Label(root, text="Hex Inspector", font=("Arial", 14))
    label.pack(pady=10)

    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_box = tk.Text(root, width=80, height=30, wrap=tk.NONE, font=("Courier", 10))
    text_box.pack(padx=10, pady=10)
    text_box.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_box.yview)

    root.mainloop()
