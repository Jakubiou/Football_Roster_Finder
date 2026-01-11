import tkinter as tk
from datetime import date, datetime
from tkinter import messagebox
from src.dao.TeamDAO import TeamDAO
from src.dao.PositionDAO import PositionDAO
from src.services.player_team_service import create_contract
from src.services.transfer_service import transfer_player

class TransferGUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db

    def open(self):
        rows = self.db.fetchall("""
               SELECT p.id, p.name, t.id, t.name
               FROM Player p
               JOIN PlayerTeam pt ON pt.player_id = p.id
               JOIN Team t ON t.id = pt.team_id
           """)

        if not rows:
            messagebox.showinfo("Info", "Žádný hráč není v týmu")
            return

        teams = TeamDAO(self.db).get_all()
        positions = PositionDAO(self.db).get_all()

        win = tk.Toplevel(self.root)
        win.title("Přestup hráče")
        win.geometry("400x550")

        player_var = tk.StringVar()
        from_team_var = tk.StringVar()
        to_team_var = tk.StringVar(value=teams[0].name)
        position_var = tk.StringVar(value=positions[0].name)

        salary_var = tk.StringVar()
        contract_type_var = tk.StringVar(value="PROFESSIONAL")
        valid_from_var = tk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        valid_to_var = tk.StringVar()

        player_map = {}
        for pid, pname, tid, tname in rows:
            player_map[pname] = (pid, tid)

        team_by_id = {t.id: t for t in teams}
        team_by_name = {t.name: t for t in teams}

        players = list(player_map.keys())
        player_var.set(players[0])

        tk.Label(win, text="Hráč").pack()
        tk.OptionMenu(win, player_var, *players).pack()

        tk.Label(win, text="Současný tým (automaticky)").pack()
        tk.Entry(win, textvariable=from_team_var, state="readonly").pack()

        def update_from_team(*_):
            _, tid = player_map[player_var.get()]
            from_team_var.set(team_by_id[tid].name)

        update_from_team()
        player_var.trace_add("write", update_from_team)

        tk.Label(win, text="Nový tým").pack()
        tk.OptionMenu(win, to_team_var, *[t.name for t in teams]).pack()

        tk.Label(win, text="Nová pozice").pack()
        tk.OptionMenu(win, position_var, *[p.name for p in positions]).pack()

        tk.Label(win, text="--- Nová smlouva ---", font=("Arial", 10, "bold")).pack(pady=(10, 5))

        tk.Label(win, text="Plat").pack()
        tk.Entry(win, textvariable=salary_var).pack()

        tk.Label(win, text="Typ smlouvy").pack()
        tk.OptionMenu(win, contract_type_var, "PROFESSIONAL", "AMATEUR", "LOAN").pack()

        tk.Label(win, text="Platnost od (YYYY-MM-DD)").pack()
        tk.Entry(win, textvariable=valid_from_var).pack()

        tk.Label(win, text="Platnost do (YYYY-MM-DD)").pack()
        tk.Entry(win, textvariable=valid_to_var).pack()

        def submit():
            try:
                pid, from_tid = player_map[player_var.get()]
                to_team = team_by_name[to_team_var.get()]
                position = next(p for p in positions if p.name == position_var.get())

                if from_tid == to_team.id:
                    raise ValueError("Hráč již v tomto týmu je")

                salary = float(salary_var.get().replace(",", "."))
                if salary < 0:
                    raise ValueError("Plat musí být kladný")

                date_from = datetime.strptime(valid_from_var.get().strip(), "%Y-%m-%d").date()
                date_to = datetime.strptime(valid_to_var.get().strip(), "%Y-%m-%d").date()

                if date_to <= date_from:
                    raise ValueError("Datum 'do' musí být po datu 'od'")

                contract_id = create_contract(self.db, salary, contract_type_var.get(), date_from, date_to)

                transfer_player(self.db, pid, from_tid, to_team.id, position.id, contract_id)
                messagebox.showinfo("OK", "Přestup proběhl úspěšně")
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Chyba", str(e))
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        tk.Button(win, text="Přestoupit", command=submit).pack(pady=15)