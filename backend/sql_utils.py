import sqlite3

db_files = {
    'TEAMS': 'databases/mlb.db',
    'BATTERS': 'databases/mlb.db',
    'PITCHERS': 'databases/mlb.db',
}


def view_database(table_name, rows=None):
    conn = sqlite3.connect(db_files[table_name])
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchmany(rows)
    for row in rows:
        print(row)
    conn.close()


def view_row_count(table_name):
    conn = sqlite3.connect(db_files[table_name])
    cursor = conn.cursor()
    cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
    row_count = cursor.fetchone()[0]
    print(f"{table_name} has {row_count} rows")
    conn.close()


def get_table(table_name, cols=None, where=None):
    db_file = db_files.get(table_name)
    if not db_file:
        return None

    # Select table data using SQL
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()  
    if cols and where:
        cursor.execute(f"""SELECT {', '.join(cols)} FROM {table_name} WHERE {where[0]} = ?""",
                       (where[1],))
    elif cols:
        cursor.execute(f"""SELECT {', '.join(cols)} FROM {table_name}""")
    elif where:
        cursor.execute(f"""SELECT * FROM {table_name} WHERE {where[0]} = ?""",
                       (where[1],))
    else:
        cursor.execute(f"""SELECT * FROM {table_name}""")
    data = cursor.fetchall()
    connection.close()
    
    # Return table as JSON
    col_names = [col[0] for col in cursor.description]
    transposed_data = list(map(list, zip(*data)))
    table_dict = dict(zip(col_names, transposed_data))
    return table_dict


def get_row(table_name, id):
    db_file = db_files.get(table_name)
    if not db_file:
        return None
    
    # Select row data using SQL
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()    
    cursor.execute(f"""SELECT * FROM {table_name} WHERE id = ?""", 
                   (id,))
    data = cursor.fetchone()
    connection.close()

    # Return row as JSON
    if not data:
        return None
    
    col_names = [col[0] for col in cursor.description]
    row_dict = dict(zip(col_names, data))
    return row_dict