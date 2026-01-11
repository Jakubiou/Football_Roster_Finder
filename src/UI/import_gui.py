import tkinter as tk
from tkinter import filedialog, messagebox
from src.services.import_service import import_players_from_csv, import_teams_from_json
from src.db.Schema import create_schema
import sys
import os


class ImportGUI:
    '''
    Handles the Graphical User Interface for data import and database maintenance.
    Provides options to import data from external files (CSV, JSON) and to
    completely reset the database schema.
    '''
    def __init__(self, root, db):
        self.root = root
        self.db = db

    def open(self):
        '''
        Opens the GUI.
        :return: None
        '''
        win = tk.Toplevel(self.root)
        win.title("Import / Reset")

        tk.Button(win, text="Import CSV", command=self.import_csv, width=20).pack(pady=5)
        tk.Button(win, text="Import JSON", command=self.import_json, width=20).pack(pady=5)
        tk.Button(win, text="Reset DB", command=self.reset_db, width=20).pack(pady=5)

    def import_csv(self):
        '''
        Imports CSV file.
        :return: None
        '''
        try:
            initial_dir = os.path.dirname(
                sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))

            path = filedialog.askopenfilename(
                title="Vyberte CSV soubor",
                filetypes=[("CSV", "*.csv")],
                initialdir=initial_dir
            )
            if path:
                import_players_from_csv(self.db, path)
                messagebox.showinfo("OK", "Import dokončen")
        except Exception as e:
            messagebox.showerror("Chyba", f"Import selhal: {str(e)}")

    def import_json(self):
        '''
        Imports JSON file.
        :return: None
        '''
        try:
            initial_dir = os.path.dirname(
                sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))

            path = filedialog.askopenfilename(
                title="Vyberte JSON soubor",
                filetypes=[("JSON", "*.json")],
                initialdir=initial_dir
            )
            if path:
                import_teams_from_json(self.db, path)
                messagebox.showinfo("OK", "Import dokončen")
        except Exception as e:
            messagebox.showerror("Chyba", f"Import selhal: {str(e)}")

    def reset_db(self):
        '''
        Resets the database schema.
        :return: None
        '''
        if messagebox.askyesno("Varování", "Smazat všechna data?"):
            try:
                create_schema(self.db)
                messagebox.showinfo("OK", "Databáze resetována")
            except Exception as e:
                messagebox.showerror("Chyba", str(e))