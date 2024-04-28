## mlb.db 
TEAMS (
    id INTEGER PRIMARY KEY,
    name TEXT(32)
)

BATTERS (
    id INTEGER PRIMARY KEY,
    team_id INTEGER,
    position TEXT(2),
    name TEXT(64),
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

PITCHERS (
    id INTEGER PRIMARY KEY,
    team_id INTEGER,
    position TEXT(1),
    name TEXT(64),
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

## app.db
USER (
    id INTEGER PRIMARY KEY,
    username TEXT(32),
    password_hash TEXT(256),
)

SEASONS (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    name TEXT(32),
)

TEAMS (
    id INTEGER PRIMARY KEY,
    season_id INTEGER FOREIGN KEY,
    name TEXT(32),
)

PITCHERS (
    id INTEGER PRIMARY KEY,
    team_id INTEGER FOREIGN KEY,
)

BATTERS (
    id INTEGER PRIMARY KEY,
    team_id INTEGER FOREIGN KEY,
)

GAMES (
    id INTEGER PRIMARY KEY,
    season_id INTEGER FOREIGN KEY,
    home_team_name TEXT(32),
    away_team_key TEXT(32),
    start_time TIMESTAMP,
)

GAMESTATES (
    id INTEGER PRIMARY KEY,
    game_id INTEGER FOREIGN KEY,
    inning TEXT(2),
    home_name: TEXT(32),
    home_score: INTEGER,
    away_name: TEXT(32),
    away_score: INTEGER,
    prediction_img TEXT(64),
    prediction_speed REAL,
    prediction_location INTEGER,
    prediction_confidence REAL,
    prediction_type TEXT(32),
    pitch_speed REAL,
    pitch_location INTEGER,
    pitch_type TEXT(32),
    pitch
    outs: INTEGER,
    balls INTEGER,
    strikes INTEGER,
    base_first TINYINT(1),
    base_second TINYINT(2),
    base_third TINYINT(3),
    pitcher_name TEXT(64),
    pitcher_img: TEXT(256),
    batter_name: TEXT(64),
    batter_img: this.current.batter.img,
)