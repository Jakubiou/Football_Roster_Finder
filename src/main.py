from src.db.Database import Database


def main():
    db = Database()

    try:
        db.connect()
        print("\nAplikace úspěšně připojena k databázi")
    except Exception as e:
        print(f"\nChyba: {e}")
    finally:
        db.disconnect()


if __name__ == "__main__":
    main()