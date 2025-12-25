from TeamDAO import TeamDAO


def main():
    dao = TeamDAO()

    team = input("Zadej název týmu: ")
    roster = dao.get_roster(team)

    if not roster:
        print("Žádní hráči nenalezeni.")
        return

    print("\nSoupiska týmu:\n")
    for p in roster:
        print(
            f"{p['player']} | {p['position']} | "
            f"{p['contract']} | {p['minutes']} min"
        )


if __name__ == "__main__":
    main()
