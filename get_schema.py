import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")
    print("-" * (len(table_name) + 6))
    
    # Get columns
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print("Columns:")
    for col in columns:
        # col: (cid, name, type, notnull, dflt_value, pk)
        print(f"  {col[1]} ({col[2]}) {'NOT NULL' if col[3] else ''} {'PRIMARY KEY' if col[5] else ''}")
    
    # Get foreign keys
    cursor.execute(f"PRAGMA foreign_key_list({table_name});")
    fks = cursor.fetchall()
    if fks:
        print("Foreign Keys:")
        for fk in fks:
            # fk: (id, seq, table, from, to, on_update, on_delete, match)
            print(f"  {fk[3]} -> {fk[2]}.{fk[4]}")
    print()