import tkinter as tk
from tkinter import messagebox
from src.dao.TeamDAO import TeamDAO
from src.dao.PositionDAO import PositionDAO
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
        contracts = self.db.fetchall("SELECT id, type FROM Contract")

        if not contracts:
            messagebox.showerror("Chyba", "Nejdříve vytvořte smlouvu")
            return

        win = tk.Toplevel(self.root)
        win.title("Přestup hráče")
        win.geometry("350x400")

        player_var = tk.StringVar()
        from_team_var = tk.StringVar()
        to_team_var = tk.StringVar(value=teams[0].name)
        position_var = tk.StringVar(value=positions[0].name)
        contract_var = tk.StringVar(value=contracts[0][1])

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

        tk.Label(win, text="Smlouva").pack()
        tk.OptionMenu(win, contract_var, *[c[1] for c in contracts]).pack()

        def submit():
            try:
                pid, from_tid = player_map[player_var.get()]
                to_team = team_by_name[to_team_var.get()]
                position = next(p for p in positions if p.name == position_var.get())
                contract = next(c for c in contracts if c[1] == contract_var.get())

                if from_tid == to_team.id:
                    raise ValueError("Hráč již v tomto týmu je")

                transfer_player(self.db, pid, from_tid, to_team.id, position.id, contract[0])
                messagebox.showinfo("OK", "Přestup proběhl úspěšně")
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Chyba", str(e))
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        tk.Button(win, text="Přestoupit", command=submit).pack(pady=15)