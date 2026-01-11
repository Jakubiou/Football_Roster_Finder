def check_tables_and_views(db, required_structure, required_views):

    needs_recreation = False

    for table_name, expected_columns in required_structure.items():
        table_exists = db.fetchone("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = ?
        """, table_name)

        if not table_exists:
            print(f"Tabulka '{table_name}' neexistuje")
            needs_recreation = True
            break

        actual_columns_rows = db.fetchall("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = ?
        """, table_name)

        actual_columns = set(row[0].lower() for row in actual_columns_rows)
        expected_columns_lower = set(col.lower() for col in expected_columns)

        if actual_columns != expected_columns_lower:
            missing = expected_columns_lower - actual_columns
            extra = actual_columns - expected_columns_lower

            print(f"Tabulka '{table_name}' má špatnou strukturu:")
            if missing:
                print(f"    Chybí sloupce: {', '.join(missing)}")
            if extra:
                print(f"    Navíc sloupce: {', '.join(extra)}")

            needs_recreation = True
            break

    if not needs_recreation:
        for view_name in required_views:
            view_exists = db.fetchone("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.VIEWS 
                WHERE TABLE_NAME = ?
            """, view_name)

            if not view_exists:
                print(f"VIEW '{view_name}' neexistuje")
                needs_recreation = True
                break

    return needs_recreation
