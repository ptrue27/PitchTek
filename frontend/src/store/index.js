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
    batter: { ...defaultBatter },
    batterIds: [],
    batterNames: [],
    pitcher: { ...defaultPitcher },
    pitcherIds: [],
    pitcherNames: [],
    teamName: "Select Team",
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
const defaultPredictions = [
    { ...defaultPrediction }, 
    { ...defaultPrediction }, 
    { ...defaultPrediction },
];

const store = createStore({
    state() {
        return {
            // host: "localhost:5000" // developent
            host: "ec2-18-208-169-218.compute-1.amazonaws.com/", // production
            isLoggedIn: localStorage.getItem("token") !== null,
            teamIds: [],
            teamNames: [],
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
            predictions: [ ...defaultPredictions ],
            seasons: localStorage.getItem("seasons") ? JSON.parse(localStorage.getItem("seasons")) : [],
            season: "Select Season",
            outs: 0,
            balls: 0,
            strikes: 0,
            bases: [false, false, false],
        }
    },
    mutations: {
        login(state, payload) {
            state.seasons = payload.seasons;
            localStorage.setItem('token', payload.token);
            localStorage.setItem('seasons', JSON.stringify(payload.seasons));
            state.isLoggedIn = true;
        },
        logout(state) {
            console.log("Logout: " + state.isLoggedIn);
            this.commit('resetDashboard');
            localStorage.removeItem('token');
            state.isLoggedIn = false;
            state.season = "Select Season";
        },
        predict(state, predictions) {
            state.predictions = predictions;
        },
        setMatchup(state, rand) {
            if(rand) {
                state.matchup = {     
                    pa: rand,
                    k: Math.floor(rand * .25),
                    bb:  Math.floor(rand * .085),
                    hits:  Math.floor(rand * .29),
                    singles:  Math.floor(rand * .14),
                    doubles:  Math.floor(rand * .05),
                    triples:  Math.floor(rand * .03),
                    hr:  Math.floor(rand * .07),
                };
            } else {
                state.matchup = { ...defaultMatchup };
            }
        },
        setSeason(state, season) {
            state.season = season;
            this.commit('resetDashboard');
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
            state.home.teamName = name;
        },
        setAwayTeamName(state, name) {
            state.away.teamName = name;
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
            state.predictions = { ...defaultPredictions };
        },
    },
});

export default store