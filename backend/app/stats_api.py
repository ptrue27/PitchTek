import pandas as pd
from baseball_id import Lookup
import mlbstatsapi
import statsapi
import datetime

mlb = mlbstatsapi.Mlb()


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


def get_image_url(mlb_id):
    espn_id = Lookup.from_mlb_ids([mlb_id])['espn_id']
    if len(espn_id.values) > 0 and not pd.isna(espn_id.values)[0]:
        image_id = espn_id.values[0]
        return f"https://a.espncdn.com/combiner/i?img=/i/headshots/mlb/players/full/{image_id}.png&w=350&h=254"
    else: 
        return ""