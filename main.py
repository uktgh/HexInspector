import tkinter as tk
import sys

from pathlib import Path
from tkinter import ttk
from ui.main_window import MainWindow

sys.path.append(str(Path(__file__).parent.parent))

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
