import tkinter as tk
from tkinter import simpledialog, messagebox
from src.dao.TeamDAO import TeamDAO
from src.models.Team import Team

class TeamGUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db

    def add_team(self):
        name = simpledialog.askstring("Tým", "Název týmu:")
        league = simpledialog.askstring("Tým", "Liga:")
        if not name:
            return
        TeamDAO(self.db).create(Team(name=name, league=league))
        messagebox.showinfo("OK", "Tým přidán")

    def show_roster(self, output):
        team_name = simpledialog.askstring("Tým", "Název týmu:")
        if not team_name:
            return

        output.delete(1.0, tk.END)
        roster = TeamDAO(self.db).get_roster(team_name)

        if not roster:
            output.insert(tk.END, "Tým nemá hráče\n")
            return

        for r in roster:
            output.insert(
                tk.END,
                f"{r['player']} | {r['position']} | {r['minutes']} min\n"
            )
