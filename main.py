import tkinter as tk
from gui import HexInspectorGUI

def main():
    root = tk.Tk()
    root.title("Hex Inspector")
    # root.iconbitmap("assets/icon.ico")
    root.after(0, HexInspectorGUI, root)  # Lazy initialization of the GUI
    root.mainloop()

if __name__ == "__main__":
    main()