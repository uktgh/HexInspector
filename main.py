import tkinter as tk
from gui import HexInspectorGUI

def main():
    root = tk.Tk()
    root.title("Hex Inspector")
    # root.iconbitmap("assets/icon.ico")
    app = HexInspectorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()