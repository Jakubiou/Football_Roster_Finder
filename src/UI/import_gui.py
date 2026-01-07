import tkinter as tk
from tkinter import filedialog, messagebox
from src.services.import_service import import_players_from_csv, import_teams_from_json
from src.db.Schema import create_schema

class ImportGUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db

    def open(self):
        win = tk.Toplevel(self.root)
        win.title("Import / Reset")

        tk.Button(win, text="Import CSV", command=self.import_csv).pack(pady=5)
        tk.Button(win, text="Import JSON", command=self.import_json).pack(pady=5)
        tk.Button(win, text="Reset DB", command=self.reset_db).pack(pady=5)

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            import_players_from_csv(self.db, path)

    def import_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            import_teams_from_json(self.db, path)

    def reset_db(self):
        if messagebox.askyesno("Reset", "Smazat DB?"):
            create_schema(self.db)
