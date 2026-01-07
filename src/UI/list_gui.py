import tkinter as tk
from src.dao.PlayerDAO import PlayerDAO
from src.dao.TeamDAO import TeamDAO

class ListGUI:
    def __init__(self, db):
        self.db = db

    def show_players(self, output: tk.Text):
        output.delete(1.0, tk.END)
        players = PlayerDAO(self.db).get_all()

        if not players:
            output.insert(tk.END, "Žádní hráči v databázi\n")
            return

        for p in players:
            output.insert(
                tk.END,
                f"ID: {p.id} | {p.name} | {p.birth_date} | {p.height} m\n"
            )

    def show_teams(self, output: tk.Text):
        output.delete(1.0, tk.END)
        teams = TeamDAO(self.db).get_all()

        if not teams:
            output.insert(tk.END, "Žádné týmy v databázi\n")
            return

        for t in teams:
            output.insert(
                tk.END,
                f"ID: {t.id} | {t.name} | {t.league}\n"
            )
