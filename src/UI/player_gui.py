from tkinter import simpledialog, messagebox
from datetime import datetime

from src.dao.PlayerDAO import PlayerDAO
from src.models.Player import Player


class PlayerGUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db

    def add_player(self):
        name = simpledialog.askstring("Hráč", "Jméno:")
        birth = simpledialog.askstring("Hráč", "Datum narození (YYYY-MM-DD):")
        height = simpledialog.askfloat("Hráč", "Výška (m):")

        try:
            player = Player(
                name=name,
                birth_date=datetime.strptime(birth, "%Y-%m-%d").date(),
                height=height,
                active=True
            )
            PlayerDAO(self.db).create(player)
            messagebox.showinfo("OK", "Hráč přidán")
        except Exception as e:
            messagebox.showerror("Chyba", str(e))
