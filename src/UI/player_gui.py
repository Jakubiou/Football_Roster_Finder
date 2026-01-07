import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date
from src.dao.PlayerDAO import PlayerDAO
from src.models.Player import Player


class PlayerGUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db

    def add_player(self):
        win = tk.Toplevel(self.root)
        win.title("Přidat hráče")
        win.geometry("300x250")

        tk.Label(win, text="Jméno a příjmení").pack()
        name_var = tk.StringVar()
        tk.Entry(win, textvariable=name_var).pack()

        tk.Label(win, text="Datum narození (YYYY-MM-DD)").pack()
        birth_var = tk.StringVar()
        tk.Entry(win, textvariable=birth_var).pack()

        tk.Label(win, text="Výška v metrech (např. 1.85)").pack()
        height_var = tk.StringVar()
        tk.Entry(win, textvariable=height_var).pack()

        def submit():
            try:
                name = name_var.get().strip()
                if len(name) < 3:
                    raise ValueError("Jméno musí mít alespoň 3 znaky")

                if not all(c.isalpha() or c.isspace() for c in name):
                    raise ValueError("Jméno může obsahovat pouze písmena a mezery")

                if not any(c.isalpha() for c in name):
                    raise ValueError("Jméno musí obsahovat alespoň jedno písmeno")

                birth_date = datetime.strptime(birth_var.get().strip(), "%Y-%m-%d").date()
                if birth_date > date.today():
                    raise ValueError("Datum narození nemůže být v budoucnosti")

                height = float(height_var.get().replace(",", "."))
                if height < 1.0 or height > 2.5:
                    raise ValueError("Výška musí být mezi 1.0 a 2.5 m")

                player = Player(name=name, birth_date=birth_date, height=height, active=True)
                PlayerDAO(self.db).create(player)
                messagebox.showinfo("OK", "Hráč přidán")
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Chyba", str(e))
            except Exception as e:
                messagebox.showerror("Chyba", f"Neplatný formát: {str(e)}")

        tk.Button(win, text="Přidat", command=submit).pack(pady=15)