import sqlite3
import os
import pandas as pd
from config import Config
from baseball_id import Lookup


db_files = {
    "TEAMS": "mlb.db",
    "BATTERS": "mlb.db",
    "PITCHERS": "mlb.db",
    "USER": "app.db",
}


def view_database(table_name, num_rows=None):
    # Print rows from a table
    conn = sqlite3.connect(os.path.join(Config.DB_DIR, db_files[table_name]))
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall() if num_rows is None else cursor.fetchmany(num_rows)
    for row in rows:
        print(row)
    conn.close()


def view_row_count(table_name):
    # Print the number of rows in a table
    conn = sqlite3.connect(os.path.join(Config.DB_DIR, db_files[table_name]))
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
    conn = sqlite3.connect(os.path.join(Config.DB_DIR, db_files[table_name]))
    cursor = conn.cursor()  
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
    conn.close()
    
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
    conn = sqlite3.connect(os.path.join(Config.DB_DIR, db_files[table_name]))
    cursor = conn.cursor()    
    cursor.execute(f"""SELECT * FROM {table_name} WHERE id = ?""", 
                   (id,))
    data = cursor.fetchone()
    conn.close()

    # Return row as JSON
    if not data:
        return None
    
    col_names = [col[0] for col in cursor.description]
    row_dict = dict(zip(col_names, data))
    row_dict['img'] = get_image_url(id)
    return row_dict


def get_image_url(mlb_id):
    espn_id = Lookup.from_mlb_ids([mlb_id])['espn_id']
    if len(espn_id.values) > 0 and not pd.isna(espn_id.values)[0]:
        image_id = espn_id.values[0]
        return f"https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/{image_id}.png&w=350&h=254"
    else: 
        return ""