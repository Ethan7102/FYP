import tkinter as tk
from tkinter import filedialog
class MakePathDialog:
    def makeDirectory(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askdirectory()
        return file_path
