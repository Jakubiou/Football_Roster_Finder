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

    def update_player(self):
        players = PlayerDAO(self.db).get_all()
        if not players:
            messagebox.showwarning("Upozornění", "Žádní hráči v databázi")
            return

        win = tk.Toplevel(self.root)
        win.title("Upravit hráče")
        win.geometry("350x300")

        tk.Label(win, text="Vyber hráče").pack()
        player_var = tk.StringVar(value=players[0].name)
        tk.OptionMenu(win, player_var, *[p.name for p in players]).pack()

        tk.Label(win, text="Nové jméno").pack()
        name_var = tk.StringVar()
        tk.Entry(win, textvariable=name_var).pack()

        tk.Label(win, text="Nové datum narození (YYYY-MM-DD)").pack()
        birth_var = tk.StringVar()
        tk.Entry(win, textvariable=birth_var).pack()

        tk.Label(win, text="Nová výška").pack()
        height_var = tk.StringVar()
        tk.Entry(win, textvariable=height_var).pack()

        def load_player_data(*args):
            selected_player = next(p for p in players if p.name == player_var.get())
            name_var.set(selected_player.name)
            birth_var.set(selected_player.birth_date.strftime("%Y-%m-%d") if selected_player.birth_date else "")
            height_var.set(str(selected_player.height))

        player_var.trace("w", load_player_data)
        load_player_data()

        def submit():
            try:
                selected_player = next(p for p in players if p.name == player_var.get())

                name = name_var.get().strip()
                if len(name) < 3:
                    raise ValueError("Jméno musí mít alespoň 3 znaky")
                if not all(c.isalpha() or c.isspace() for c in name):
                    raise ValueError("Jméno může obsahovat pouze písmena a mezery")

                birth_date = datetime.strptime(birth_var.get().strip(), "%Y-%m-%d").date()
                if birth_date > date.today():
                    raise ValueError("Datum narození nemůže být v budoucnosti")

                height = float(height_var.get().replace(",", "."))
                if height < 1.0 or height > 2.5:
                    raise ValueError("Výška musí být mezi 1.0 a 2.5 m")

                selected_player.name = name
                selected_player.birth_date = birth_date
                selected_player.height = height

                PlayerDAO(self.db).update(selected_player)
                messagebox.showinfo("OK", "Hráč upraven")
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Chyba", str(e))
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        tk.Button(win, text="Uložit změny", command=submit).pack(pady=15)

    def delete_player(self):
        players = PlayerDAO(self.db).get_all()
        if not players:
            messagebox.showwarning("Upozornění", "Žádní hráči v databázi")
            return

        win = tk.Toplevel(self.root)
        win.title("Odebrat hráče")
        win.geometry("300x150")

        tk.Label(win, text="Vyber hráče k odebrání").pack()
        player_var = tk.StringVar(value=players[0].name)
        tk.OptionMenu(win, player_var, *[p.name for p in players]).pack()

        def submit():
            try:
                if messagebox.askyesno("Potvrzení", f"Opravdu smazat hráče {player_var.get()}?"):
                    selected_player = next(p for p in players if p.name == player_var.get())
                    PlayerDAO(self.db).delete(selected_player.id)
                    messagebox.showinfo("OK", "Hráč odstraněn")
                    win.destroy()
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        tk.Button(win, text="Odebrat", command=submit, bg="#f44336", fg="white").pack(pady=15)