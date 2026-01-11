import sys
import os
from src.UI.main_gui import tk, App
from tkinter import messagebox


def get_base_path():
    '''
    Determines the base directory of the application.
    Handles both standard script execution and frozen executables (e.g., PyInstaller).
    :return: The absolute path to the directory containing the application.
    '''
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    try:
        base_path = get_base_path()
        os.chdir(base_path)

        root = tk.Tk()
        App(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Chyba", f"Aplikace selhala: {str(e)}")
        sys.exit(1)