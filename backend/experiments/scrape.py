import sqlite3
from app import stats_api
import mlbstatsapi
import time
from random import uniform

mlb = mlbstatsapi.Mlb()
DATE = '10/01/2023'
SEASON = 2023


def rest(rest_time=5):
    time.sleep(rest_time + uniform(0, 2))


def remake_tables():
    db_file = stats_api.db_files["TEAMS"]
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # TEAMS
    cursor.execute("DROP TABLE IF EXISTS TEAMS")
    cursor.execute("""
        CREATE TABLE TEAMS (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)

    # BATTERS
    cursor.execute("DROP TABLE IF EXISTS BATTERS")
    cursor.execute("""
        CREATE TABLE BATTERS (
            id INTEGER PRIMARY KEY,
            team_id INTEGER,
            position TEXT,
            name TEXT,
            img TEXT,
            games INTEGER,
            pa INTEGER,
            avg REAL,
            obp REAL,
            slg REAL,
            ops REAL,
            hits INTEGER,
            hr INTEGER
        )
    """)

    # PITCHERS
    cursor.execute("DROP TABLE IF EXISTS PITCHERS")
    cursor.execute("""
        CREATE TABLE PITCHERS (
            id INTEGER PRIMARY KEY,
            team_id INTEGER,
            position TEXT,
            name TEXT,
            img TEXT,
            games INTEGER,
            batters INTEGER,
            whip REAL,
            era REAL,
            kper9 REAL,
            bbper9 REAL,
            hits INTEGER,
            hr INTEGER
        )
    """)

    conn.commit()
    conn.close()


def get_teams():
    """Populate the TEAMS table of the teams database.
    """
    table_name = "TEAMS"
    db_file = stats_api.db_files[table_name]
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Insert data into the TEAMS table
    teams = mlb.get_teams()
    for team in teams:
        cursor.execute(f'''
            INSERT OR IGNORE INTO {table_name} (id, name)
            VALUES (?, ?)
        ''', (team.id, team.name))

    print(f'Finished scraping data for {table_name}')
    conn.commit()
    conn.close()


def get_rosters(min_team_id=0):
    """Populate the BATTERS and PITCHERS tables.
    """
    db_file = stats_api.db_files["BATTERS"]
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get team ids
    team_ids = stats_api.get_table("TEAMS")["id"]
    team_ids = [id for id in sorted(team_ids) if id > min_team_id]

    positions = {
        '1': "P", 
        '2': "C", 
        '3': "1B", 
        '4': "2B", 
        '5': "3B", 
        '6': "SS", 
        '7': "LF", 
        '8': "CF", 
        '9': "RF",
    }
    for team_id in team_ids:
        # Get team roster
        roster = mlb.get_team_roster(team_id, date=DATE)
        for player in roster: # player(id, fullname, primaryposition.code)

            # Get player position
            position = positions[player.primaryposition.code] if player.primaryposition.code in positions.keys() else "DH"

            # Get batter data
            if (position != "P") or (player.fullname == "Shohei Ohtani"):
                stats = mlb.get_player_stats(player.id, stats=["season"], groups=["hitting"], season=SEASON)
                if len(stats) == 0:
                    continue

                stats = stats["hitting"]["season"].splits[0]
                stat = stats.stat
                img = "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/30836.png"

                cursor.execute("""
                    INSERT OR IGNORE INTO BATTERS (
                        id, 
                        team_id, 
                        position, 
                        name, 
                        img, 
                        games, 
                        pa, 
                        avg, 
                        obp, 
                        slg, 
                        ops,
                        hits, 
                        hr
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        player.id,
                        team_id, 
                        position,
                        player.fullname, 
                        img, 
                        stat.gamesplayed, 
                        stat.plateappearances, 
                        stat.avg, 
                        stat.obp, 
                        stat.slg, 
                        stat.ops, 
                        stat.hits, 
                        stat.homeruns
                    )
                )

            # Get pitcher data
            if position == "P":
                stats = mlb.get_player_stats(player.id, stats=["season"], groups=["pitching"], season=SEASON)
                if len(stats) == 0:
                    continue

                stats = stats["pitching"]["season"].splits[0]
                stat = stats.stat
                img = "https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/30836.png"
                
                cursor.execute("""
                    INSERT OR IGNORE INTO PITCHERS (
                        id, 
                        team_id, 
                        position, 
                        name, 
                        img, 
                        games, 
                        batters, 
                        whip, 
                        era, 
                        kper9, 
                        bbper9,
                        hits, 
                        hr
                    ) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        player.id,
                        team_id, 
                        position,
                        player.fullname, 
                        img, 
                        stat.gamespitched, 
                        stat.battersfaced, 
                        stat.whip, 
                        stat.era, 
                        stat.strikeoutsper9inn, 
                        stat.walksper9inn, 
                        stat.hits, 
                        stat.homeruns
                    )
                )

        conn.commit()
        print("Scraped roster data for teams through", team_id)
        
        rest(20)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    try:
        #remake_tables()
        #get_teams()
        get_rosters(139)

    except KeyboardInterrupt:
        print("Interrupted") 