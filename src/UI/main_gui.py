import tkinter as tk
from src.db.Database import Database
from src.db.Schema import ensure_schema
from src.UI.player_gui import PlayerGUI
from src.UI.team_gui import TeamGUI
from src.UI.player_team_gui import PlayerTeamGUI
from src.UI.transfer_gui import TransferGUI
from src.UI.contract_gui import ContractGUI
from src.UI.report_gui import ReportGUI
from src.UI.import_gui import ImportGUI
from src.UI.list_gui import ListGUI



class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Football Roster")
        self.root.geometry("900x950")

        self.db = Database()
        self.db.connect()
        ensure_schema(self.db)

        self.output = tk.Text(self.root, height=22)
        self.output.pack(fill=tk.BOTH, padx=10, pady=10)

        self.create_ui()

    def create_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        list_gui = ListGUI(self.db)
        player_gui = PlayerGUI(self.root, self.db)
        team_gui = TeamGUI(self.root, self.db)
        pt = PlayerTeamGUI(self.root, self.db)

        buttons = [
            ("Zobrazit hráče", lambda: list_gui.show_players(self.output)),
            ("Zobrazit týmy", lambda: list_gui.show_teams(self.output)),
            ("Přidat hráče", player_gui.add_player),
            ("Upravit hráče", player_gui.update_player),
            ("Odebrat hráče", player_gui.delete_player),
            ("Přidat tým", team_gui.add_team),
            ("Zobrazit soupisku", lambda: TeamGUI(self.root, self.db).show_roster(self.output)),
            ("Přidat hráče do týmu", pt.add_player),
            ("Odebrat hráče z týmu", pt.remove_player),
            ("Aktualizovat minuty", pt.update_minutes),
            ("Přestup hráče", lambda: TransferGUI(self.root, self.db).open()),
            ("Smlouvy", lambda: ContractGUI(self.root, self.db).open()),
            ("Statistický report", lambda: ReportGUI(self.db).show(self.output)),
            ("Import / Reset", lambda: ImportGUI(self.root, self.db).open())
        ]

        for text, cmd in buttons:
            tk.Button(frame, text=text, width=35, command=cmd).pack(pady=2)
