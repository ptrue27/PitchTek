import sqlite3
import sql_utils
import mlbstatsapi
import time
from random import uniform
import os

mlb = mlbstatsapi.Mlb()


def rest():
    time.sleep(5 + uniform(0, 2))


def get_teams():
    """Populate the TEAMS table of the teams database.
    """
    table_name = 'TEAMS'
    db_file = sql_utils.db_files[table_name]
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create TEAMS table if it doesn't exist
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')

    # Insert data into the TEAMS table
    teams = mlb.get_teams()
    for team in teams:
        cursor.execute(f'''
            INSERT OR IGNORE INTO {table_name} (id, name)
            VALUES (?, ?)
        ''', (team.id, team.name))

    print(f'Updated {table_name}')
    conn.commit()
    conn.close()


def get_rosters():
    """Populate the ROSTERS table of the teams database.
    """
    table_name = 'ROSTERS'
    db_file = sql_utils.db_files[table_name]
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create ROSTERS table if it doesn't exist
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            name TEXT,
            position INTEGER,
            team_id INTEGER
        )
    ''')

    # Insert data into the ROSTERS table
    teams_table_name = 'TEAMS'
    teams = sql_utils.get_table(teams_table_name)
    for team_id in teams['id']:
        roster = mlb.get_team_roster(team_id)
        for player in roster:
            cursor.execute(f'''
                INSERT OR IGNORE INTO {table_name} (id, name, position, team_id)
                VALUES (?, ?, ?, ?)
            ''', (player.id, player.fullname, player.primaryposition.code, team_id))
        print(f'Updated {table_name} for team {team_id}')
        rest()

    conn.commit()
    conn.close()


if __name__ == '__main__':
    get_teams()
    get_rosters()