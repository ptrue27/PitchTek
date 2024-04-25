import sqlite3
import os
import pandas as pd
from config import Config
from baseball_id import Lookup
import mlbstatsapi
import statsapi
import datetime

mlb = mlbstatsapi.Mlb()
db_files = {
    "TEAMS": "mlb.db",
    "BATTERS": "mlb.db",
    "PITCHERS": "mlb.db",
    "USER": "app.db",
    "SEASONS": "app.db",
}


def get_teams(year):
    ids, names = [], []
    for team in mlb.get_teams(season=year):
        ids.append(team.id)
        names.append(team.name)
    return ids, names


def get_roster(team_id, year):
        current_time = datetime.datetime.now()
        if year == current_time.year: 
            formatted_date = current_time.strftime("%m/%d/%Y")
        else:
            formatted_date = f"10/01/{year}"
            
        roster = mlb.get_team_roster(team_id, date=formatted_date)
        pitcher_ids, pitcher_names = [], []
        batter_ids, batter_names = [], []

        for player in roster:
            if player.primaryposition.code == '1':
                pitcher_ids.append(player.id)
                pitcher_names.append(player.fullname)
                if player.fullname == "Shohei Ohtani":
                    batter_ids.append(player.id)
                    batter_names.append(player.fullname)
            else:
                batter_ids.append(player.id)
                batter_names.append(player.fullname)
                
        return {"ids": pitcher_ids, "names": pitcher_names}, \
               {"ids": batter_ids, "names": batter_names}


def get_pitcher(id, year):
    data = mlb.get_player_stats(id, stats=["season"], groups=["pitching"], season=year)
    data = data["pitching"]["season"].splits[0]
    stats = data.stat
    return {
        "id": id,
        "name": data.player.fullname,
        "img": get_image_url(int(id)),
        "games": stats.gamespitched,
        "batters": stats.battersfaced,
        "whip": stats.whip,
        "era": stats.era,
        "kper9": stats.strikeoutsper9inn,
        "bbper9": stats.walksper9inn,
        "hits": stats.hits,
        "hr": stats.homeruns,
    }


def get_batter(id, year):
    data = mlb.get_player_stats(id, stats=["season"], groups=["hitting"], season=year)
    data = data["hitting"]["season"].splits[0]
    stats = data.stat
    return {
        "id": id,
        "name": data.player.fullname,
        "img": get_image_url(int(id)),
        "games": stats.gamesplayed,
        "pa": stats.plateappearances,
        "avg": stats.avg,
        "obp": stats.obp,
        "slg": stats.slg,
        "ops": stats.ops,
        "hits": stats.hits,
        "hr": stats.homeruns,
    }


def get_versus(batter_id, pitcher_id):
    # Retrieve versus stats
    hydrate = f'stats(group=[hitting],type=[vsPlayer],opposingPlayerId={pitcher_id},sportId=1)'
    params = {'personId': batter_id, 'hydrate': hydrate}
    data = statsapi.get('person', params)
    splits = data['people'][0]['stats'][0]['splits']

    # Handle no history
    if len(splits) == 0:
        return {"pa": '-', "k": '-', "bb": '-', "hits": '-', "singles": '-',
                "doubles": '-', "triples": '-', "hr": '-',
    }
    
    # Parse versus stats
    total_stats = splits[0]['stat']
    return {
        "pa": total_stats["plateAppearances"],
        "k": total_stats["strikeOuts"],
        "bb": total_stats["baseOnBalls"],
        "hits": total_stats["hits"],
        "singles": total_stats["hits"] - total_stats["doubles"] - \
            total_stats["triples"] - total_stats["homeRuns"],
        "doubles": total_stats["doubles"],
        "triples": total_stats["triples"],
        "hr": total_stats["homeRuns"],
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