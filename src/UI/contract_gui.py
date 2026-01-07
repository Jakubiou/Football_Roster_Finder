import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from src.dao.PlayerDAO import PlayerDAO
from src.services.player_team_service import create_contract, assign_contract_to_player


class ContractGUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db

    def open(self):
        players = PlayerDAO(self.db).get_all()
        if not players:
            messagebox.showerror("Chyba", "Nejdříve přidejte hráče")
            return

        win = tk.Toplevel(self.root)
        win.title("Vytvořit smlouvu")
        win.geometry("300x350")

        tk.Label(win, text="Hráč").pack()
        player_var = tk.StringVar(value=players[0].name)
        tk.OptionMenu(win, player_var, *[p.name for p in players]).pack()

        tk.Label(win, text="Plat (pouze číslo)").pack()
        salary_var = tk.StringVar()
        tk.Entry(win, textvariable=salary_var).pack()

        tk.Label(win, text="Typ smlouvy").pack()
        type_var = tk.StringVar(value="PROFESSIONAL")
        tk.OptionMenu(win, type_var, "PROFESSIONAL", "AMATEUR", "LOAN").pack()

        tk.Label(win, text="Od (YYYY-MM-DD)").pack()
        from_var = tk.StringVar()
        tk.Entry(win, textvariable=from_var).pack()

        tk.Label(win, text="Do (YYYY-MM-DD)").pack()
        to_var = tk.StringVar()
        tk.Entry(win, textvariable=to_var).pack()

        def submit():
            try:
                salary = float(salary_var.get().replace(",", "."))
                if salary < 0:
                    raise ValueError("Plat musí být kladný")

                date_from = datetime.strptime(from_var.get().strip(), "%Y-%m-%d").date()
                date_to = datetime.strptime(to_var.get().strip(), "%Y-%m-%d").date()

                if date_to <= date_from:
                    raise ValueError("Datum 'do' musí být po datu 'od'")

                player = next(p for p in players if p.name == player_var.get())
                contract_id = create_contract(self.db, salary, type_var.get(), date_from, date_to)
                assign_contract_to_player(self.db, player.id, contract_id)

                messagebox.showinfo("OK", "Smlouva vytvořena")
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Chyba", str(e))
            except Exception as e:
                messagebox.showerror("Chyba", f"Neplatný formát dat: {str(e)}")

        tk.Button(win, text="Uložit", command=submit).pack(pady=15)