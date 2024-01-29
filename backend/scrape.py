import sqlite3
import sql_utils
import mlbstatsapi
import time
import os

mlb = mlbstatsapi.Mlb()
REST_TIME = 10
DATA_DIR = 'databases'

DB_TEAMS = 'teams.db'
TABLE_TEAMS = 'TEAMS' # (id, name)
TABLE_ROSTERS = 'ROSTERS' # (id, name, position, team_id)

DB_PLAYERS = 'players.db'
TABLE_BATTERS = 'BATTERS' # (id, name, img, hr, obp, slg)
TABLE_PITCHERS = 'PITCHERS' # (id, name, img, era, kper9, bbper9)


def get_teams():
    """Populate the TEAMS table of the teams database.
    """
    conn = sqlite3.connect(os.path.join(DATA_DIR, DB_TEAMS))
    cursor = conn.cursor()

    # Create TEAMS table if it doesn't exist
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_TEAMS} (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')

    # Insert data into the TEAMS table
    teams = mlb.get_teams()
    for team in teams:
        cursor.execute(f'''
            INSERT INTO {TABLE_TEAMS} (id, name)
            VALUES (?, ?)
        ''', (team.id, team.name))
    print(f'Scraped {DB_TEAMS} {TABLE_TEAMS}')

    conn.commit()
    conn.close()


def get_rosters():
    """Populate the ROSTERS table of the teams database.
    """
    conn = sqlite3.connect(os.path.join(DATA_DIR, DB_TEAMS))
    cursor = conn.cursor()

    # Create TEAMS table if it doesn't exist
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_ROSTERS} (
            id INTEGER PRIMARY KEY,
            name TEXT,
            position INTEGER,
            team_id INTEGER
        )
    ''')

    # Insert data into the TEAMS table
    teams = sql_utils.get_table(DB_TEAMS, TABLE_TEAMS)
    for team_id in teams['id']:
        roster = mlb.get_team_roster(team_id)
        for player in roster:
            cursor.execute(f'''
                INSERT INTO {TABLE_ROSTERS} (id, name, position, team_id)
                VALUES (?, ?, ?, ?)
            ''', (player.id, player.fullname, player.primaryposition.code, team_id))
        print(f'Scraped {DB_TEAMS} {TABLE_ROSTERS} {team_id}')
        time.sleep(REST_TIME)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    get_teams()
    get_rosters()