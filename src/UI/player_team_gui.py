import tkinter as tk
from tkinter import messagebox
from src.dao.PlayerDAO import PlayerDAO
from src.dao.TeamDAO import TeamDAO
from src.dao.PositionDAO import PositionDAO
from src.services.player_team_service import add_player_to_team, remove_player_from_team, update_minutes


class PlayerTeamGUI:
    '''
    Handles the Graphical User Interface for managing player-team assignments.
    Provides functionality to add players to teams, remove them, and track
    their performance (minutes played).
    '''
    def __init__(self, root, db):
        self.root = root
        self.db = db

    def add_player(self):
        '''
        Adds a player to the team.
        :return: None
        '''
        players = PlayerDAO(self.db).get_all()
        teams = TeamDAO(self.db).get_all()
        positions = PositionDAO(self.db).get_all()

        if not players or not teams or not positions:
            messagebox.showerror("Chyba", "Nejdříve přidejte hráče, týmy a pozice")
            return

        win = tk.Toplevel(self.root)
        win.title("Přidat hráče do týmu")

        pv, tv, posv = tk.StringVar(value=players[0].name), tk.StringVar(value=teams[0].name), tk.StringVar(
            value=positions[0].name)

        tk.Label(win, text="Hráč").pack()
        tk.OptionMenu(win, pv, *[p.name for p in players]).pack()

        tk.Label(win, text="Tým").pack()
        tk.OptionMenu(win, tv, *[t.name for t in teams]).pack()

        tk.Label(win, text="Pozice").pack()
        tk.OptionMenu(win, posv, *[p.name for p in positions]).pack()

        def submit():
            try:
                player = next(p for p in players if p.name == pv.get())
                team = next(t for t in teams if t.name == tv.get())
                position = next(p for p in positions if p.name == posv.get())

                add_player_to_team(self.db, player.id, team.id, position.id)
                messagebox.showinfo("OK", "Hráč přidán do týmu")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        tk.Button(win, text="Přidat", command=submit).pack(pady=10)

    def remove_player(self):
        '''
        Removes a player from the team.
        :return: None
        '''
        teams = TeamDAO(self.db).get_all()
        if not teams:
            messagebox.showerror("Chyba", "Žádné týmy")
            return

        win = tk.Toplevel(self.root)
        win.title("Odebrat hráče")

        team_var = tk.StringVar(value=teams[0].name)
        player_var = tk.StringVar()

        tk.Label(win, text="Tým").pack()
        tk.OptionMenu(win, team_var, *[t.name for t in teams]).pack()

        tk.Label(win, text="Hráč").pack()
        player_menu = tk.OptionMenu(win, player_var, "")
        player_menu.pack()

        def load_players(*_):
            team = next(t for t in teams if t.name == team_var.get())
            players = TeamDAO(self.db).get_players_in_team(team.id)
            menu = player_menu["menu"]
            menu.delete(0, "end")
            if players:
                player_var.set(players[0][1])
                for pid, pname in players:
                    menu.add_command(label=pname, command=lambda v=pname: player_var.set(v))

        team_var.trace("w", load_players)
        load_players()

        def submit():
            try:
                if not player_var.get():
                    raise ValueError("Vyberte hráče")
                team = next(t for t in teams if t.name == team_var.get())
                players = TeamDAO(self.db).get_players_in_team(team.id)
                player_id = next(pid for pid, pname in players if pname == player_var.get())
                remove_player_from_team(self.db, player_id, team.id)
                messagebox.showinfo("OK", "Hráč odebrán")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        tk.Button(win, text="Odebrat", command=submit).pack(pady=10)

    def update_minutes(self):
        '''
        Updates the minutes played for the team.
        :return: None
        '''
        teams = TeamDAO(self.db).get_all()
        if not teams:
            messagebox.showerror("Chyba", "Žádné týmy")
            return

        win = tk.Toplevel(self.root)
        win.title("Aktualizace minut")

        team_var = tk.StringVar(value=teams[0].name)
        player_var = tk.StringVar()
        mins_var = tk.StringVar()

        tk.Label(win, text="Tým").pack()
        tk.OptionMenu(win, team_var, *[t.name for t in teams]).pack()

        tk.Label(win, text="Hráč").pack()
        player_menu = tk.OptionMenu(win, player_var, "")
        player_menu.pack()

        tk.Label(win, text="Přidat minut (celé číslo)").pack()
        tk.Entry(win, textvariable=mins_var).pack()

        def load_players(*_):
            team = next(t for t in teams if t.name == team_var.get())
            players = TeamDAO(self.db).get_players_in_team(team.id)
            menu = player_menu["menu"]
            menu.delete(0, "end")
            if players:
                player_var.set(players[0][1])
                for pid, pname in players:
                    menu.add_command(label=pname, command=lambda v=pname: player_var.set(v))

        team_var.trace("w", load_players)
        load_players()

        def submit():
            try:
                if not player_var.get():
                    raise ValueError("Vyberte hráče")
                minutes = int(mins_var.get())
                if minutes < 0:
                    raise ValueError("Minuty musí být kladné číslo")

                team = next(t for t in teams if t.name == team_var.get())
                players = TeamDAO(self.db).get_players_in_team(team.id)
                player_id = next(pid for pid, pname in players if pname == player_var.get())
                update_minutes(self.db, player_id, team.id, minutes)
                messagebox.showinfo("OK", "Minuty aktualizovány")
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Chyba", str(e))
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        tk.Button(win, text="Uložit", command=submit).pack(pady=10)