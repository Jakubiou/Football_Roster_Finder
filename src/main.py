from src.db.Database import Database
from src.db.Schema import create_schema


def main():
    db = Database()

    try:
        db.connect()
        create_schema(db)
        print("\nDatabázová struktura úspěšně vytvořena")
    except Exception as e:
        print(f"\nChyba: {e}")
    finally:
        db.disconnect()


if __name__ == "__main__":
    main()