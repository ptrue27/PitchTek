import sqlite3


db_files = {
    'TEAMS': 'databases/teams.db',
    'ROSTERS': 'databases/teams.db',
    'BATTERS': 'databases/players.db',
    'PITCHERS': 'databases/players.db',
}


def get_table(table_name):
    db_file = db_files.get(table_name)
    if not db_file:
        return None

    # Select table data using SQL
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
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
    cursor.execute(f'SELECT * FROM {table_name} WHERE id = ?', (id,))
    data = cursor.fetchone()
    connection.close()

    # Return row as JSON
    if not data:
        return None
    
    col_names = [col[0] for col in cursor.description]
    row_dict = dict(zip(col_names, data))
    return row_dict