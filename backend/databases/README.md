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