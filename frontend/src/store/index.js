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
const defaultManage = {
    seasonName: "Select Season",
    teamName: "Select Team",
    gameName: "Select Game",
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
            // host: "pitchtek.pro", // production
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
            season: {
                ids: localStorage.getItem("seasonIds") ? JSON.parse(localStorage.getItem("seasonIds")) : [],
                names: localStorage.getItem("seasonNames") ? JSON.parse(localStorage.getItem("seasonNames")) : [],
                id: 0,
                name: "Select Season"
            },
            outs: 0,
            balls: 0,
            strikes: 0,
            bases: [false, false, false],
            manage: { ...defaultManage },
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
            console.log("Logout: " + state.isLoggedIn);
            this.commit('resetDashboard');
            state.manage = { ...defaultManage };
            localStorage.removeItem('token');
            state.isLoggedIn = false;
            state.season.name = "Select Season";
        },
        setGameId(state, gameId) {
            state.gameId = gameId;
        },
        setManageSeason(state, season) {
            state.manage.seasonName = season;
            state.manage.teamName = "Select Team";
            state.manage.gameName = "Select Game";
            state.manage.pitcherNames = [];
            state.manage.batterNames = [];
            state.manage.gameStates = [];
        },
        setManageTeam(state, team) {
            state.manage.teamName = team;
        },
        setManageGame(state, game) {
            state.manage.gameName = game;
        },
        setManagerTeams(state, teams) {
            state.manage.teamIds = teams.ids;
            state.manage.teamNames = teams.names;
        },
        setManagerGames(state, games) {
            state.manage.gameIds = games.ids;
            state.manage.gameNames = games.names;
        },
        setManagerRoster(state, roster) {
            state.manage.pitcherNames = roster.pitchers.names;
            state.manage.batterNames = roster.batters.names;
        },
        setManagerGameStates(state, gameStates) {
            state.manage.gameStates = gameStates;
        },
        setRecording(state, isRecording) {
            state.recording = isRecording;
        },
        predict(state, prediction) {
            state.prediction = prediction;
        },
        setMatchup(state, matchup) {
            if(matchup) {
                state.matchup = matchup;
            } else {
                state.matchup = { ...defaultMatchup };
            }
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
        },
    },
    
});

export default store