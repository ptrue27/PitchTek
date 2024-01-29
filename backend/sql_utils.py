import sqlite3

# SQLite database file
PLAYERS_DB = '\databases\players.db'


def get_table(database, table):
    # Select table data using SQL
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {table}')
    data = cursor.fetchall()
    connection.close()
    
    # Return table as JSON
    col_names = [col[0] for col in cursor.description]
    transposed_data = list(map(list, zip(*data)))
    table_dict = dict(zip(col_names, transposed_data))
    return table_dict


def get_row(database, table_name, id):
    # Select row data using SQL
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {table_name} WHERE id = ?', (id,))
    data = cursor.fetchone()
    connection.close()

    # Return row as JSON
    col_names = [col[0] for col in cursor.description]
    row_dict = dict(zip(col_names, data))
    return row_dict



