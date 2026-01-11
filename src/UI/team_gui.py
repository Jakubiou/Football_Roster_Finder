import tkinter as tk
from tkinter import messagebox
from src.dao.TeamDAO import TeamDAO
from src.models.Team import Team


class TeamGUI:
    '''
    Handles the Graphical User Interface for team management.
    Provides functionality to add new teams and display current team rosters
    based on activity and minutes played.
    '''
    def __init__(self, root, db):
        self.root = root
        self.db = db

    def add_team(self):
        '''
        Adds a new team to the database.
        :return: None
        '''
        win = tk.Toplevel(self.root)
        win.title("Přidat tým")
        win.geometry("300x200")

        tk.Label(win, text="Název týmu").pack()
        name_var = tk.StringVar()
        tk.Entry(win, textvariable=name_var).pack()

        tk.Label(win, text="Liga (zadej číslo 1 nebo 2)").pack()
        league_var = tk.StringVar()
        tk.Entry(win, textvariable=league_var).pack()

        def submit():
            try:
                name = name_var.get().strip()

                if len(name) < 2:
                    raise ValueError("Název musí mít alespoň 2 znaky")

                league_input = league_var.get().strip()
                if league_input not in ['1', '2']:
                    raise ValueError("Liga musí být číslo 1 nebo 2")

                league = f"{league_input}. LIGA"

                TeamDAO(self.db).create(Team(name=name, league=league))
                messagebox.showinfo("OK", f"Tým přidán do {league}")
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Chyba", str(e))
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        tk.Button(win, text="Přidat", command=submit).pack(pady=15)

    def show_roster(self, output):
        '''
        Opens a team selector window. Upon selection, retrieves the roster
        for the given team and displays it in the main output text widget.
        :param output: The main Tkinter Text widget for data output.
        :return: None
        '''
        teams = TeamDAO(self.db).get_all()
        if not teams:
            messagebox.showwarning("Upozornění", "Žádné týmy v databázi")
            return

        win = tk.Toplevel(self.root)
        win.title("Zobrazit soupisku")
        win.geometry("300x150")

        tk.Label(win, text="Vyberte tým").pack()
        team_var = tk.StringVar(value=teams[0].name)
        tk.OptionMenu(win, team_var, *[t.name for t in teams]).pack()

        def show():
            roster = TeamDAO(self.db).get_roster(team_var.get())
            output.delete(1.0, tk.END)
            output.insert(tk.END, f"Soupiska: {team_var.get()}\n\n")

            if not roster:
                output.insert(tk.END, "Žádní hráči kteří by měli odehrané nějaké minuty nebo bz bzli aktivní\n")
            else:
                for r in roster:
                    output.insert(tk.END, f"{r['player']} | {r['position']} | {r['minutes']} min\n")
            win.destroy()

        tk.Button(win, text="Zobrazit", command=show).pack(pady=10)