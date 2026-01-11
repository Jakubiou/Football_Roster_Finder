import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from src.dao.ContractDAO import ContractDAO
from src.dao.PlayerDAO import PlayerDAO
from src.services.player_team_service import create_contract, assign_contract_to_player


class ContractGUI:
    '''
    Handles the Graphical User Interface for contract management.
    Allows users to view, create, update, and delete player contracts
    through a series of Tkinter TopLevel windows.
    '''
    def __init__(self, root, db):
        self.root = root
        self.db = db

    def open(self):
        '''
        Opens the graphical user interface.
        :return: None
        '''
        win = tk.Toplevel(self.root)
        win.title("Správa smluv")
        win.geometry("300x250")

        tk.Label(win, text="Správa smluv", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Button(win, text="Zobrazit všechny smlouvy", command=self.show_contracts, width=25).pack(pady=5)
        tk.Button(win, text="Vytvořit novou smlouvu", command=self.create_contract, width=25).pack(pady=5)
        tk.Button(win, text="Upravit smlouvu", command=self.update_contract, width=25).pack(pady=5)
        tk.Button(win, text="Smazat smlouvu", command=self.delete_contract, width=25).pack(pady=5)

    def show_contracts(self):
        '''
        Displays a window with a formatted overview of all contracts
        retrieved from the V_PlayerContracts database view.
        :return: None
        '''
        win = tk.Toplevel(self.root)
        win.title("Přehled smluv")
        win.geometry("600x300")

        tk.Label(win, text="Všechny smlouvy").pack()

        text = tk.Text(win, height=15, width=70)
        text.pack(padx=10, pady=10)

        try:
            rows = self.db.fetchall("SELECT player, type, salary FROM V_PlayerContracts")

            if not rows:
                text.insert(tk.END, "Žádné smlouvy\n")
            else:
                for r in rows:
                    text.insert(tk.END, f"{r[0]} | {r[1]} | {r[2]} Kč\n")
        except:
            text.insert(tk.END, "Chyba načítání\n")

        text.config(state=tk.DISABLED)

    def create_contract(self):
        '''
        Opens a form to create a new contract. Includes input validation
        for salary amounts and date ranges.
        :return: None
        '''
        players = PlayerDAO(self.db).get_all()
        if not players:
            messagebox.showerror("Chyba", "Nejdříve přidejte hráče")
            return

        win = tk.Toplevel(self.root)
        win.title("Vytvořit smlouvu")
        win.geometry("300x350")

        tk.Label(win, text="Hráč").pack()
        player_var = tk.StringVar(value=players[0].name)
        tk.OptionMenu(win, player_var, *[p.name for p in players]).pack()

        tk.Label(win, text="Plat (pouze číslo)").pack()
        salary_var = tk.StringVar()
        tk.Entry(win, textvariable=salary_var).pack()

        tk.Label(win, text="Typ smlouvy").pack()
        type_var = tk.StringVar(value="PROFESSIONAL")
        tk.OptionMenu(win, type_var, "PROFESSIONAL", "AMATEUR", "LOAN").pack()

        tk.Label(win, text="Od (YYYY-MM-DD)").pack()
        from_var = tk.StringVar()
        tk.Entry(win, textvariable=from_var).pack()

        tk.Label(win, text="Do (YYYY-MM-DD)").pack()
        to_var = tk.StringVar()
        tk.Entry(win, textvariable=to_var).pack()

        def submit():
            '''
            Internal helper to validate inputs and call the service
            layer to persist the contract and its assignment.
            :return: None
            '''
            try:
                salary = float(salary_var.get().replace(",", "."))
                if salary < 0:
                    raise ValueError("Plat musí být kladný")

                date_from = datetime.strptime(from_var.get().strip(), "%Y-%m-%d").date()
                date_to = datetime.strptime(to_var.get().strip(), "%Y-%m-%d").date()

                if date_to <= date_from:
                    raise ValueError("Datum 'do' musí být po datu 'od'")

                player = next(p for p in players if p.name == player_var.get())
                contract_id = create_contract(self.db, salary, type_var.get(), date_from, date_to)
                assign_contract_to_player(self.db, player.id, contract_id)

                messagebox.showinfo("OK", "Smlouva vytvořena")
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Chyba", str(e))
            except Exception as e:
                messagebox.showerror("Chyba", f"Neplatný formát dat: {str(e)}")

        tk.Button(win, text="Uložit", command=submit).pack(pady=15)

    def update_contract(self):
        '''
        Updates the contract table.
        :return: None
        '''
        contracts = ContractDAO(self.db).get_all()
        if not contracts:
            messagebox.showwarning("Upozornění", "Žádné smlouvy v databázi")
            return

        win = tk.Toplevel(self.root)
        win.title("Upravit smlouvu")
        win.geometry("350x400")

        tk.Label(win, text="Vyberte smlouvu").pack()
        contract_var = tk.StringVar()
        contract_options = [f"ID:{c.id} - {c.type} - {c.salary} Kč" for c in contracts]
        contract_var.set(contract_options[0])
        tk.OptionMenu(win, contract_var, *contract_options).pack()

        tk.Label(win, text="Nový plat").pack()
        salary_var = tk.StringVar()
        tk.Entry(win, textvariable=salary_var).pack()

        tk.Label(win, text="Nový typ").pack()
        type_var = tk.StringVar(value="PROFESSIONAL")
        tk.OptionMenu(win, type_var, "PROFESSIONAL", "AMATEUR", "LOAN").pack()

        tk.Label(win, text="Od (YYYY-MM-DD)").pack()
        from_var = tk.StringVar()
        tk.Entry(win, textvariable=from_var).pack()

        tk.Label(win, text="Do (YYYY-MM-DD)").pack()
        to_var = tk.StringVar()
        tk.Entry(win, textvariable=to_var).pack()

        def load_contract_data(*args):
            '''
            Pre-fills the form fields based on the selected contract.
            :param args:
            :return: None
            '''
            selected_idx = contract_options.index(contract_var.get())
            contract = contracts[selected_idx]
            salary_var.set(str(contract.salary))
            type_var.set(contract.type)
            from_var.set(contract.valid_from.strftime("%Y-%m-%d"))
            to_var.set(contract.valid_to.strftime("%Y-%m-%d"))

        contract_var.trace("w", load_contract_data)
        load_contract_data()

        def submit():
            '''
            Internal helper to validate inputs and call the service
            :return: None
            '''
            try:
                selected_idx = contract_options.index(contract_var.get())
                contract = contracts[selected_idx]

                salary = float(salary_var.get().replace(",", "."))
                if salary < 0:
                    raise ValueError("Plat musí být kladný")

                date_from = datetime.strptime(from_var.get().strip(), "%Y-%m-%d").date()
                date_to = datetime.strptime(to_var.get().strip(), "%Y-%m-%d").date()

                if date_to <= date_from:
                    raise ValueError("Datum 'do' musí být po datu 'od'")

                contract.salary = salary
                contract.type = type_var.get()
                contract.valid_from = date_from
                contract.valid_to = date_to

                ContractDAO(self.db).update(contract)
                messagebox.showinfo("OK", "Smlouva upravena")
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Chyba", str(e))
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        tk.Button(win, text="Uložit změny", command=submit).pack(pady=15)

    def delete_contract(self):
        '''
        Opens a window to delete a contract. Includes a confirmation
        dialog and handles cascade deletion of links in PlayerContract.
        :return: None
        '''
        contracts = ContractDAO(self.db).get_all()
        if not contracts:
            messagebox.showwarning("Upozornění", "Žádné smlouvy v databázi")
            return

        win = tk.Toplevel(self.root)
        win.title("Smazat smlouvu")
        win.geometry("350x200")

        tk.Label(win, text="Vyberte smlouvu ke smazání").pack()
        contract_var = tk.StringVar()
        contract_options = [f"ID:{c.id} - {c.type} - {c.salary} Kč" for c in contracts]
        contract_var.set(contract_options[0])
        tk.OptionMenu(win, contract_var, *contract_options).pack()

        def submit():
            '''
            Executes deletion after user confirmation.
            :return: None
            '''
            try:
                if messagebox.askyesno("Potvrzení",
                                       f"Opravdu smazat smlouvu {contract_var.get()}?\n\nPozor: Smaže se i vazba v PlayerContract!"):
                    selected_idx = contract_options.index(contract_var.get())
                    contract = contracts[selected_idx]

                    self.db.execute("DELETE FROM PlayerContract WHERE contract_id = ?", contract.id)
                    self.db.commit()

                    ContractDAO(self.db).delete(contract.id)
                    messagebox.showinfo("OK", "Smlouva a vazby smazány")
                    win.destroy()
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        tk.Button(win, text="Smazat", command=submit, bg="#f44336", fg="white").pack(pady=15)