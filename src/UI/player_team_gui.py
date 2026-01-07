import tkinter as tk
from tkinter import messagebox, simpledialog
from src.dao.PlayerDAO import PlayerDAO
from src.dao.TeamDAO import TeamDAO
from src.dao.PositionDAO import PositionDAO
from src.services.player_team_service import add_player_to_team,remove_player_from_team, update_minutes,change_position



class PlayerTeamGUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db

    def add_player(self):
        players = PlayerDAO(self.db).get_all()
        teams = TeamDAO(self.db).get_all()
        positions = PositionDAO(self.db).get_all()

        win = tk.Toplevel(self.root)
        win.title("Přidat hráče do týmu")

        pv, tv, posv = tk.StringVar(), tk.StringVar(), tk.StringVar()

        tk.Label(win, text="Hráč").pack()
        tk.OptionMenu(win, pv, *[p.name for p in players]).pack()

        tk.Label(win, text="Tým").pack()
        tk.OptionMenu(win, tv, *[t.name for t in teams]).pack()

        tk.Label(win, text="Pozice").pack()
        tk.OptionMenu(win, posv, *[p.name for p in positions]).pack()

        def submit():
            player = next(p for p in players if p.name == pv.get())
            team = next(t for t in teams if t.name == tv.get())
            position = next(p for p in positions if p.name == posv.get())

            add_player_to_team(self.db, player.id, team.id, position.id)
            messagebox.showinfo("OK", "Hráč přidán do týmu")
            win.destroy()

        tk.Button(win, text="Přidat", command=submit).pack(pady=10)

    def remove_player(self):
        pid = simpledialog.askinteger("Odebrat", "ID hráče:")
        tid = simpledialog.askinteger("Odebrat", "ID týmu:")

        remove_player_from_team(self.db, pid, tid)
        messagebox.showinfo("OK", "Hráč odebrán")

    def change_position(self):
        teams = TeamDAO(self.db).get_all()
        positions = PositionDAO(self.db).get_all()

        win = tk.Toplevel(self.root)
        win.title("Změna pozice")

        team_var = tk.StringVar()
        player_var = tk.StringVar()
        pos_var = tk.StringVar()

        tk.Label(win, text="Tým").pack()
        tk.OptionMenu(win, team_var, *[t.name for t in teams]).pack()

        player_menu = tk.OptionMenu(win, player_var, "")
        player_menu.pack()

        tk.Label(win, text="Nová pozice").pack()
        tk.OptionMenu(win, pos_var, *[p.name for p in positions]).pack()

        def load_players(*_):
            team = next(t for t in teams if t.name == team_var.get())
            players = TeamDAO(self.db).get_players_in_team(team.id)

            menu = player_menu["menu"]
            menu.delete(0, "end")

            for pid, pname in players:
                menu.add_command(
                    label=pname,
                    command=lambda v=pname: player_var.set(v)
                )

        team_var.trace("w", load_players)

        def submit():
            team = next(t for t in teams if t.name == team_var.get())
            players = TeamDAO(self.db).get_players_in_team(team.id)
            player_id = next(pid for pid, pname in players if pname == player_var.get())
            position = next(p for p in positions if p.name == pos_var.get())

            change_position(self.db, player_id, position.id)
            messagebox.showinfo("OK", "Pozice změněna")
            win.destroy()

        tk.Button(win, text="Uložit", command=submit).pack(pady=10)

    def update_minutes(self):
        teams = TeamDAO(self.db).get_all()

        win = tk.Toplevel(self.root)
        win.title("Aktualizace minut")

        team_var = tk.StringVar()
        player_var = tk.StringVar()
        mins_var = tk.IntVar()

        tk.Label(win, text="Tým").pack()
        tk.OptionMenu(win, team_var, *[t.name for t in teams]).pack()

        player_menu = tk.OptionMenu(win, player_var, "")
        player_menu.pack()

        tk.Label(win, text="Přidat minut").pack()
        tk.Entry(win, textvariable=mins_var).pack()

        def load_players(*_):
            team = next(t for t in teams if t.name == team_var.get())
            players = TeamDAO(self.db).get_players_in_team(team.id)

            menu = player_menu["menu"]
            menu.delete(0, "end")

            for pid, pname in players:
                menu.add_command(
                    label=pname,
                    command=lambda v=pname: player_var.set(v)
                )

        team_var.trace("w", load_players)

        def submit():
            team = next(t for t in teams if t.name == team_var.get())
            players = TeamDAO(self.db).get_players_in_team(team.id)
            player_id = next(pid for pid, pname in players if pname == player_var.get())

            update_minutes(self.db, player_id, team.id, mins_var.get())
            messagebox.showinfo("OK", "Minuty aktualizovány")
            win.destroy()

        tk.Button(win, text="Uložit", command=submit).pack(pady=10)
