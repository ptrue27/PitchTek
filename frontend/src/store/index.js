import { createStore } from 'vuex';

const defaultBatter = {
    id: 0, 
    team_id: 0,
    position: '-',
    name: "Select Batter", 
    img: "data:image/png;base64,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",
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
    img: "data:image/png;base64,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",
    games: '-', 
    batters: '-', 
    whip: '-', 
    era: '-', 
    kper9: '-', 
    bbper9: '-',
    hits: '-', 
    hr: '-',
};

const store = createStore({
    state() {
        return {
            inning: "1∧",
            default: {
                batter: { ...defaultBatter },
                pitcher: { ...defaultPitcher },
            },
            home: {
                batter: { ...defaultBatter },
                batterIds: [],
                batterNames: [],
                pitcher: { ...defaultPitcher },
                pitcherIds: [],
                pitcherNames: [],
            },
            away: {
                batter: { ...defaultBatter },
                batterIds: [],
                batterNames: [],
                pitcher: { ...defaultPitcher },
                pitcherIds: [],
                pitcherNames: [],
            },
            current: {
                batter: { ...defaultBatter },
                batterIds: [],
                batterNames: [],
                pitcher: { ...defaultPitcher },
                pitcherIds: [],
                pitcherNames: [],
            },
            predictionImgSrc: "@/assets/strikezone.jpg",
        }
    },
    mutations: {
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
        setHome(state, home) {
            state.home.batter = { ...defaultBatter };
            state.home.batterIds = home.batterIds;
            state.home.batterNames = home.batterNames;
            state.home.pitcher = { ...defaultPitcher };
            state.home.pitcherIds = home.pitcherIds;
            state.home.pitcherNames = home.pitcherNames;
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
    },
});

export default store