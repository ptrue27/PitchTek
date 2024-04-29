import sqlite3
import os
from config import Config


def get_cols(table, cols, where_col, where_value, sort="ASC"):
    conn = sqlite3.connect(os.path.join(Config.DB_DIR, Config.APP_DB))
    cursor = conn.cursor()

    # SQL query to fetch all records
    select_query = f"""
        SELECT {", ".join(cols)}
        FROM {table}
        WHERE {where_col} = ?
        ORDER BY id {sort}
    """
    cursor.execute(select_query, (where_value,))
    records = cursor.fetchall()

    # Separate the cols into distinct lists
    num_cols = len(cols)
    lists = [[] for i in range(num_cols)]
    for row in records:
        for i in range(num_cols):
            lists[i].append(row[i])

    # Close the connection
    cursor.close()
    conn.close()

    return lists


def get_records(table, where_col, where_value, sort="ASC"):
    conn = sqlite3.connect(os.path.join(Config.DB_DIR, Config.APP_DB))
    cursor = conn.cursor()

    # Get the column names from the table schema
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [info[1] for info in cursor.fetchall()]

    # SQL query to fetch all records
    select_query = f"""
        SELECT *
        FROM {table}
        WHERE {where_col} = ?
        ORDER BY id {sort}
    """
    cursor.execute(select_query, (where_value,))
    records = cursor.fetchall()

    # Close the connection
    conn.close()
    return [dict(zip(columns, record)) for record in records]


def insert_record(table, record, get_id=False):
    conn = sqlite3.connect(os.path.join(Config.DB_DIR, Config.APP_DB))
    cursor = conn.cursor()

    # SQL query to insert a new record
    keys, vals = record.keys(), list(record.values())
    insert_query = f"""
        INSERT INTO {table} ({", ".join(keys)}) 
        VALUES ({", ".join(['?' for i in keys])})
    """
    cursor.execute(insert_query, vals)
    conn.commit()

    # Get the ID of the newly inserted record if requested
    if get_id:
        new_season_id = cursor.lastrowid
        conn.close()
        return new_season_id
    
    conn.close()


def record_exists(table, record):
    # Connect to the SQLite database
    conn = sqlite3.connect(os.path.join(Config.DB_DIR, Config.APP_DB))
    cursor = conn.cursor()

    # SQL query to check if a record exists
    keys, vals = record.keys(), list(record.values())
    check_query = f"""
        SELECT COUNT(1)
        FROM {table}
        WHERE {" AND ".join([f"{col} = ?" for col in keys])}
    """
    
    # Execute the query with the given value
    cursor.execute(check_query, vals)
    record_count = cursor.fetchone()[0]

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # If the count is greater than 0, the record exists
    return record_count > 0


def delete_record(table, record, get_id=False):
    # Connect to the SQLite database
    conn = sqlite3.connect(os.path.join(Config.DB_DIR, Config.APP_DB))
    cursor = conn.cursor()

    if get_id:
        # SQL query to get a record
        keys, vals = record.keys(), list(record.values())
        check_query = f"""
            SELECT id
            FROM {table}
            WHERE {" AND ".join([f"{col} = ?" for col in keys])}
        """
        cursor.execute(check_query, vals)
        record_id = cursor.fetchone()[0]

    # SQL query to delete a record
    del_query = f"""
        DELETE FROM {table}
        WHERE {" AND ".join([f"{col} = ?" for col in keys])}
    """
    cursor.execute(del_query, vals)
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    if get_id:
        return record_id
   

def print_table(table_name, num_rows=None):
    # Print rows from a table
    conn = sqlite3.connect(os.path.join(Config.DB_DIR, Config.APP_DB))
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall() if num_rows is None else cursor.fetchmany(num_rows)
    for row in rows:
        print(row)
    conn.close()


def print_num_rows(table_name):
    # Print the number of rows in a table
    conn = sqlite3.connect(os.path.join(Config.DB_DIR, Config.APP_DB))
    cursor = conn.cursor()
    cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
    row_count = cursor.fetchone()[0]
    print(f"{table_name} has {row_count} rows")
    conn.close()


def print_schema():
    # Connect to the SQLite database
    db_path = os.path.join(Config.DB_DIR, Config.APP_DB)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to get all table names in the database
    table_query = """
        SELECT name 
        FROM sqlite_master 
        WHERE type = 'table' AND 
            name NOT LIKE 'sqlite_%'
    """
    
    cursor.execute(table_query)
    table_names = cursor.fetchall()

    # Retrieve the schema for each table
    for table in table_names:
        table_name = table[0]  # Get the table name from the tuple
        schema_query = f"PRAGMA table_info({table_name})"
        
        cursor.execute(schema_query)
        columns = cursor.fetchall()

        print(f"Schema for table: {table_name}")
        print(f"{'Column Name':<15} {'Data Type':<15}")
        
        for column in columns:
            #col_name, data_type, not_null, default_value, primary_key = column
            #not_null_str = "NO" if not_null == 1 else "YES"
            #primary_key_str = "YES" if primary_key == 1 else "NO"
            #print(f"{col_name:<15} {data_type:<15} {not_null_str:<10} {default_value:<20} {primary_key_str}")
            print(column[1:3])
        print(" ")

    # Close the cursor and the connection
    cursor.close()
    conn.close()
