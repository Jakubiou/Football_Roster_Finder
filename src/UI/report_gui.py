from src.services.report_service import generate_team_statistics
import tkinter as tk


class ReportGUI:
    def __init__(self, db):
        self.db = db

    def show(self, output):
        output.delete(1.0, tk.END)
        for r in generate_team_statistics(self.db):
            output.insert(
                tk.END,
                f"{r['team']} | hráči: {r['players']} | plat: {r['total_salary']}\n"
            )
