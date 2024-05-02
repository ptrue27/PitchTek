import { createStore } from 'vuex';

const defaultBatter = {
    id: 0, 
    team_id: 0,
    position: '-',
    name: "Select Batter", 
    img: "",
    games: '-', 
    pa: '-', 
    avg: '-', 
    obp: '-', 
    slg: '-', 
    ops: '-',
    hits: '-', 
    hr: '-',
};
const defaultPitcher = {
    id: 0, 
    team_id: 0,
    position: '-',
    name: "Select Pitcher", 
    img: "",
    games: '-', 
    batters: '-', 
    whip: '-', 
    era: '-', 
    kper9: '-', 
    bbper9: '-',
    hits: '-', 
    hr: '-',
};
const defaultTeam = {
    id: 0,
    name: "Select Team",
    batter: { ...defaultBatter },
    batterIds: [],
    batterNames: [],
    pitcher: { ...defaultPitcher },
    pitcherIds: [],
    pitcherNames: [],
    score: 0,
};
const defaultMatchup = {
    pa: '-',
    k: '-',
    bb: '-',
    hits: '-',
    singles: '-',
    doubles: '-',
    triples: '-',
    hr: '-',
};
const defaultPrediction = {
    img: "default_heat_map.jpg",
    speed: '-',
    location: '-',
    confidence: '-',
    type: '-',
};
const defaultAccount = {
    seasonName: "Select Season",
    seasonId: 0, 
    teamName: "Select Team",
    teamId: 0,
    gameName: "Select Game",
    gameId: 0,
    teamNames: [],
    teamIds: [],
    pitcherNames: [],
    batterNames: [],
    gameNames: [],
    gameIds: [],
    gameStates: [],
};

const store = createStore({
    state() {
        return { 
            host: "localhost:5000", // development
            //host: "pitchtek.pro", // production
            isLoggedIn: localStorage.getItem("token") !== null,
            recording: false,
            teamIds: [],
            teamNames: [],
            gameId: 0,
            inning: "1∧",
            default: {
                batter: { ...defaultBatter },
                pitcher: { ...defaultPitcher },
                matchup: { ...defaultMatchup },
            },
            home: { ...defaultTeam },
            away: { ...defaultTeam },
            current: { ...defaultTeam },
            matchup: { ...defaultMatchup },
            prediction: { ...defaultPrediction },
            gameStates: [],
            season: {
                id: 0,
                name: "Select Season",
                ids: localStorage.getItem("seasonIds") ? 
                    JSON.parse(localStorage.getItem("seasonIds")) : [],
                names: localStorage.getItem("seasonNames") ? 
                    JSON.parse(localStorage.getItem("seasonNames")) : [],
            },
            balls: 0,
            strikes: 0,
            bases: [false, false, false],
            release_speed: 0,
            plate_x: 0,
            plate_z: 2.49,
            account: { ...defaultAccount },
        }
    },
    mutations: {
        login(state, payload) {
            state.isLoggedIn = true;
            localStorage.setItem('token', payload.token);
            state.season.ids = payload.season_ids;
            localStorage.setItem('seasonIds', JSON.stringify(payload.season_ids));
            state.season.names = payload.season_names;
            localStorage.setItem('seasonNames', JSON.stringify(payload.season_names));
        },
        logout(state) {
            // Update localStorage
            localStorage.removeItem('token');
            localStorage.removeItem('seasonIds');
            localStorage.removeItem('seasonNames');

            // Update store
            this.commit('resetDashboard');
            state.isLoggedIn = false;
            state.season = {
                id: 0,
                name: "Select Season",
                ids: [],
                names: [],
            };
            state.account = { ...defaultAccount };
        },
        setAccountSeason(state, seasonName) {
            state.account = { ...defaultAccount };
            state.account.seasonName = seasonName;
            const index = state.season.names.indexOf(seasonName);
            state.account.seasonId = state.season.ids[index];
        },
        addSeason(state, season) {
            // Update localStorage
            let seasonIds = JSON.parse(localStorage.getItem("seasonIds"));
            seasonIds.push(season.id);
            localStorage.setItem("seasonIds", JSON.stringify(seasonIds));
            let seasonNames = JSON.parse(localStorage.getItem("seasonNames"));
            seasonIds.push(season.name);
            localStorage.setItem("seasonNames", JSON.stringify(seasonNames));
            
            // Update store
            state.season.ids.push(season.id);
            state.season.names.push(season.name);
        },
        deleteSeason(state, season) {
            // Update localStorage
            let seasonIds = JSON.parse(localStorage.getItem("seasonIds"));
            seasonIds = seasonIds.filter(i => i != season.id);
            localStorage.setItem("seasonIds", JSON.stringify(seasonIds));
            let seasonNames = JSON.parse(localStorage.getItem("seasonNames"));
            seasonNames = seasonNames.filter(i => i != season.name);
            localStorage.setItem("seasonNames", JSON.stringify(seasonNames));
            
            // Update store
            state.season.ids = seasonIds;
            state.season.names = seasonNames;
            state.account = { ...defaultAccount };

            // Update Dashboard
            if (state.season.id == season.id) {
                this.commit('resetDashboard');
                state.recording = false;
                state.season.id = 0;
                state.season.name = "Select Season"
            }
        },
        setAccountTeams(state, teams) {
            state.account.teamIds = teams.ids;
            state.account.teamNames = teams.names;
        },
        setAccountTeam(state, teamName) {
            state.account.teamName = teamName;
            const index = state.account.teamNames.indexOf(teamName);
            state.account.teamId = state.account.teamIds[index];
        },
        addTeam(state, team) {
            // Update Account
            state.account.teamIds.push(team.id);
            state.account.teamNames.push(team.name);

            // Update Dashboard
            if(state.season.id == state.account.seasonId) {
                state.teamIds.push(team.id);
                state.teamNames.push(team.name);
            }
        },
        deleteTeam(state, team) {
            // Update Account
            const teamIds = state.account.teamIds.filter(i => i != team.id);
            state.account.teamIds = teamIds;
            const teamNames = state.account.teamNames.filter(i => i != team.name);
            state.account.teamNames = teamNames;
            state.account.teamName = "Select Team";
            state.account.teamId = 0;
            state.account.pitcherIds = [];
            state.account.pitcherNames = [];
            state.account.batterIds = [];
            state.account.batterNames = [];

            // Update Dashboard
            if(state.season.id == state.account.seasonId) {
                state.teamIds = teamIds;
                state.teamNames = teamNames;
            }
        },
        setAccountRoster(state, roster) {
            state.account.pitcherNames = roster.pitchers.names;
            state.account.batterNames = roster.batters.names;
        },
        setAccountGames(state, games) {
            state.account.gameIds = games.ids;
            state.account.gameNames = games.names;
        },
        setAccountGame(state, game) {
            state.account.gameName = game;
        },
        setAccountGameStates(state, gameStates) {
            state.account.gameStates = gameStates;
        },
        setRecording(state, isRecording) {
            state.recording = isRecording;
            if (!isRecording) {
                state.gameId = 0;
                state.gameStates = [];
            }
        },
        predict(state, prediction) {
            state.prediction = prediction;
            state.gameStates.push({
                inning: state.inning,
                home_name: state.home.name,
                home_score: state.home.score,
                away_name: state.away.name,
                away_score: state.away.score,
                prediction_img: prediction.img,
                prediction_speed: prediction.speed,
                prediction_location: prediction.location,
                prediction_confidence: prediction.confidence,
                prediction_type: prediction.type,
                outs: state.outs,
                balls: state.balls,
                strikes: state.strikes,
                base_first: state.bases[0],
                base_second: state.bases[1],
                base_third: state.bases[2],
                pitcher_name: state.current.pitcher.name,
                pitcher_img: state.current.pitcher.img,
                batter_name: state.current.batter.name,
                batter_img: state.current.batter.img,
            });
        },
        setMatchup(state, matchup) {
            if(matchup) {
                state.matchup = matchup;
            } else {
                state.matchup = { ...defaultMatchup };
            }
        },
        setGameId(state, gameId) {
            state.gameId = gameId;
        },
        setSeasonName(state, seasonName) {
            this.commit('resetDashboard');
            state.season.name = seasonName;
        },
        setSeasonId(state, seasonId) {
            state.season.id = seasonId;
        },
        setTeamIds(state, ids) {
            state.teamIds = ids;
        },
        setTeamNames(state, names) {
            state.teamNames = names;
        },
        setInning(state, inning) {
            state.inning = inning;
            if (inning.includes('∨')) {
                state.current.batter = state.home.batter;
                state.current.batterIds = state.home.batterIds;
                state.current.batterNames = state.home.batterNames;
                state.current.pitcher = state.away.pitcher;
                state.current.pitcherIds = state.away.pitcherIds;
                state.current.pitcherNames = state.away.pitcherNames;
            }
            else {
                state.current.batter = state.away.batter;
                state.current.batterIds = state.away.batterIds;
                state.current.batterNames = state.away.batterNames;
                state.current.pitcher = state.home.pitcher;
                state.current.pitcherIds = state.home.pitcherIds;
                state.current.pitcherNames = state.home.pitcherNames;
            }
        },
        setOuts(state, outs) {
            state.outs = outs;
        },
        setBalls(state, balls) {
            state.balls = balls;
        },
        setStrikes(state, strikes) {
            state.strikes = strikes;
        },
        toggleBase(state, index) {
            state.bases[index] = !state.bases[index];
        },
        setCurrentBatter(state, batter) {
            state.current.batter = batter;
            if (state.inning.includes('∨')) {
                state.home.batter = batter;
            }
            else {
                state.away.batter = batter;
            }
        },
        setCurrentPitcher(state, pitcher) {
            state.current.pitcher = pitcher;
            if (state.inning.includes('∨')) {
                state.away.pitcher = pitcher;
            }
            else {
                state.home.pitcher = pitcher;
            }
        },
        setHomeTeamName(state, name) {
            state.home.name = name;
        },
        setAwayTeamName(state, name) {
            state.away.name = name;
        },
        setHomeScore(state, score) {
            state.home.score = score;
        },
        setAwayScore(state, score) {
            state.away.score = score;
        },
        setReleaseSpeed(state, speed) {
            state.release_speed = speed;
        },
        setPlateX(state, x) {
            state.plate_x = x;
        },
        setPlateZ(state, z) {
            state.plate_z = z;
        },
        setHome(state, home) {
            state.home.batter = { ...defaultBatter };
            state.home.batterIds = home.batterIds;
            state.home.batterNames = home.batterNames;
            state.home.pitcher = { ...defaultPitcher };
            state.home.pitcherIds = home.pitcherIds;
            state.home.pitcherNames = home.pitcherNames;
            state.home.score = home.score;
            state.home.id = home.id;
            state.matchup = { ...defaultMatchup };
            if (state.inning.includes('∨')) {
                state.current.batter = { ...defaultBatter };
                state.current.batterIds = home.batterIds;
                state.current.batterNames = home.batterNames;
            }
            else {      
                state.current.pitcher = { ...defaultPitcher };
                state.current.pitcherIds = home.pitcherIds;
                state.current.pitcherNames = home.pitcherNames;
            }
        },
        setAway(state, away) {
            state.away.batter = { ...defaultBatter };
            state.away.batterIds = away.batterIds;
            state.away.batterNames = away.batterNames;
            state.away.pitcher = { ...defaultPitcher };
            state.away.pitcherIds = away.pitcherIds;
            state.away.pitcherNames = away.pitcherNames;
            state.away.score = away.score;
            state.away.id = away.id;
            state.matchup = { ...defaultMatchup };
            if (state.inning.includes('∧')) {
                state.current.batter = { ...defaultBatter };
                state.current.batterIds = away.batterIds;
                state.current.batterNames = away.batterNames;
            }
            else {
                state.current.pitcher = { ...defaultPitcher };
                state.current.pitcherIds = away.pitcherIds;
                state.current.pitcherNames = away.pitcherNames;
            }
        },
        resetDashboard(state) {
            state.inning = "1∧";
            state.home = { ...defaultTeam };
            state.away = { ...defaultTeam };
            state.current = { ...defaultTeam };
            state.matchup = { ...defaultMatchup };
            state.outs = 0;
            state.balls = 0;
            state.strikes = 0;
            state.bases = [false, false, false];
            state.prediction = { ...defaultPrediction };
            state.gameId = 0;
            state.gameStates = [];
        },
    },
    created() {
        // Load data from localStorage
        const storedName = localStorage.getItem("userName");
        if (storedName) {
          this.userName = storedName;  // Restore from localStorage
        }
    },
    methods: {
        saveUserName() {
          // Save to localStorage
          localStorage.setItem("userName", this.userName);
        },
    },
    
});

export default store