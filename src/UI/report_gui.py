from src.services.report_service import generate_team_statistics
import tkinter as tk


class ReportGUI:
    '''
    Handles the Graphical User Interface for displaying analytical reports.
    Aggregates database statistics and renders them into a text-based format
    for the user.
    '''
    def __init__(self, db):
        self.db = db

    def show(self, output):
        '''
        Clears the provided text widget and populates it with team-level
        statistics including player counts and financial totals.
        :param output: The Tkinter Text widget where the report will be rendered.
        :return: None
        '''
        output.delete(1.0, tk.END)
        for r in generate_team_statistics(self.db):
            output.insert(
                tk.END,
                f"{r['team']} | hráči: {r['players']} | plat: {r['total_salary']}\n"
            )
