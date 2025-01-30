import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path

# Aggiungi il path del progetto al PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from ui.main_window import MainWindow

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
