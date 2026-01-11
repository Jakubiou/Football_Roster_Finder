# Football Roster Finder

Aplikace pro správu fotbalových týmů a hráčů s databázovým úložištěm.

## Rychlé spuštění

### Požadavky:
- Windows OS
- SQL Server s ODBC Driver 17
- Soubor `config.json` ve stejné složce jako exe soubor

### Postup:
1. **Upravte config.json** - Zadejte své databázové údaje
2. **Spusťte FootballRoster.exe**
3. **Při prvním spuštění** se automaticky vytvoří databázová struktura


## Konfigurace (config.json)

```json
{
  "connectionString": "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=football;UID=user;PWD=password"
}
```

**Upravte:**
- `SERVER` - adresa SQL serveru
- `DATABASE` - název databáze
- `UID` - uživatelské jméno
- `PWD` - heslo

## Import testovacích dat

### Formát CSV (hráči):
```csv
name,birth_date,height,active
Jan Novák,15.05.1995,1.85,1
Petr Svoboda,20.08.1998,1.78,1
```

### Formát JSON (týmy):
```json
[
  {"name": "Slavia Praha", "league": "1. LIGA"},
  {"name": "Sparta Praha", "league": "1. LIGA"}
]
```

## Hlavní funkce

1. **Správa hráčů** - Přidání, zobrazení, import z CSV
2. **Správa týmů** - Vytváření týmů, přiřazování hráčů
3. **Přestupy** - Převod hráčů mezi týmy (s transakcí)
4. **Smlouvy** - Vytváření, úprava, mazání a přiřazování smluv
5. **Statistiky** - Agregované reporty z více tabulek
6. **Import** - CSV a JSON podpora

## Validace vstupů

- **Jméno hráče:** Pouze písmena a mezery
- **Datum:** Formát YYYY-MM-DD
- **Výška:** 1.0 - 2.5 metrů
- **Liga:** Pouze číslo 1 nebo 2
- **Minuty:** Kladná celá čísla

## Řešení problémů

### "Config soubor nenalezen"
- Ujistěte se, že `config.json` je ve stejné složce jako .exe

### "Chyba připojení k databázi"
- Zkontrolujte:
1. Je SQL Server spuštěný?
2. Jsou přihlašovací údaje v config.json správné?
3. Je nainstalován ODBC Driver 17?

### "ODBC Driver not found"
→ Nainstalujte: [ODBC Driver 17 for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

### Program se okamžitě zavře
→ Spusťte z příkazové řádky pro zobrazení chyb:
```bash
FootballRoster.exe
```

## Databázová struktura

Program automaticky vytvoří:
- **6 tabulek:** Team, Player, Position, Contract, PlayerTeam, PlayerContract
- **4 pohledy (VIEW):** V_TeamRoster, V_TeamStatistics, V_CurrentRoster, V_PlayerContracts
- **Vazbu M:N** mezi Player a Contract
