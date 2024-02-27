## mlb.db 
TEAMS (
    id INTEGER PRIMARY KEY,
    name TEXT
)

BATTERS (
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

PITCHERS (
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