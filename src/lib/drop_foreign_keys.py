def drop_foreign_keys(db):

    print("Odstraňuji FOREIGN KEY constrainty")

    drop_fks = """
    DECLARE @sql NVARCHAR(MAX) = N'';

    SELECT @sql += 'ALTER TABLE ' + QUOTENAME(OBJECT_SCHEMA_NAME(parent_object_id))
        + '.' + QUOTENAME(OBJECT_NAME(parent_object_id))
        + ' DROP CONSTRAINT ' + QUOTENAME(name) + ';'
    FROM sys.foreign_keys;

    EXEC sp_executesql @sql;
    """

    try:
        db.execute(drop_fks)
        db.commit()
    except Exception as e:
        print(f"Chyba při odstraňování FK: {e}")
