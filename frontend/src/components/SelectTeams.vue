<template>
    <!--Team selection-->
    <v-row class="text-center" style="margin-bottom: -40px; margin-left: 3px; margin-top: 3px; margin-right: 3px;">
        <!--Input home team-->
        <v-col cols="6">
            <v-select
                :items="homeTeamNames" 
                v-model="homeTeamName"
                @update:modelValue="handleHomeTeamChange"
                variant="solo-filled" 
                density="compact"
                color="green-darken-1"
                :disabled="this.$store.state.recording"
            ></v-select>
        </v-col>
                  
        <!--Input away team-->
        <v-col cols="6">
            <v-select
                :items="awayTeamNames" 
                v-model="awayTeamName"
                @update:modelValue="handleAwayTeamChange"
                variant="solo-filled" 
                density="compact"
                color="green-darken-1"
                :disabled="this.$store.state.recording"
            ></v-select>
        </v-col>
     </v-row>
              
    <!--Score input-->
    <v-row style="margin-bottom: -30px;">
        <!--Home Score-->
        <v-col cols="3" style="margin-top: 10px;" align="right">
            <p class="home-away" style="margin-right: 30px;">
                Home
            </p>
        </v-col>
        <v-col cols="2">
            <v-select
                :items="scores"
                v-model="homeScore"
                density="compact"
                variant="solo-filled"
                color="green-darken-1"
            ></v-select>
        </v-col>

        <v-col cols="2" class="score-spacer text-center">
            <p>-</p>
        </v-col>
        
        <!--Away Score-->
        <v-col cols="2">
            <v-select
                :items="scores"
                v-model="awayScore"
                density="compact"
                variant="solo-filled"
                color="green-darken-1"
            ></v-select>
        </v-col>
        <v-col cols="3" style="margin-top: 10px;" align="left">
            <p class="home-away" style="margin-left: 30px;">
                Away
            </p>
        </v-col>
    </v-row>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
        scores: [],
    };
  },
  methods: {
    handleHomeTeamChange() {
      const index = this.$store.state.teamNames.indexOf(this.homeTeamName);
      const teamId = this.$store.state.teamIds[index];
      const path = 'http://' + this.$store.state.host + '/api/get_roster';
      const params = {
        season_name: this.$store.state.season.name,
        team_id: teamId
      };

      axios.get(path, { params })
        .then((res) => {
          const roster = res.data;
          console.log("Loaded roster for " + teamId + ": " + 
            roster.batters.ids.length + " batters, " +
            roster.pitchers.ids.length + " pitchers"
          );
          const newHome = {
            batterIds: roster.batters.ids, 
            batterNames: roster.batters.names,
            pitcherIds: roster.pitchers.ids,
            pitcherNames: roster.pitchers.names,
            score: 0,
            id: teamId,
          };
          this.$store.commit("setHome", newHome);
        })
        .catch((error) => {
            console.error("Error loading roster for " + teamId + ": " + error);
            const newHome = {
              batterIds: [], 
              batterNames: [], 
              pitcherIds: [], 
              pitcherNames: [],
              score: 0,
              id: 0
            };
            this.$store.commit("setHomeTeamName", "Select Team");
            this.$store.commit("setHome", newHome);
        });
    },
    handleAwayTeamChange() {
      const index = this.$store.state.teamNames.indexOf(this.awayTeamName);
      const teamId = this.$store.state.teamIds[index];
      const path = 'http://' + this.$store.state.host + '/api/get_roster';
      const params = {
        season_name: this.$store.state.season.name,
        team_id: teamId
      };

      axios.get(path, { params })
        .then((res) => {
          const roster = res.data;
          console.log("Loaded roster for " + teamId + ": " + 
            roster.batters.ids.length + " batters, " +
            roster.pitchers.ids.length + " pitchers"
          );
          const newAway = {
            batterIds: roster.batters.ids, 
            batterNames: roster.batters.names,
            pitcherIds: roster.pitchers.ids,
            pitcherNames: roster.pitchers.names,
            score: 0,
            id: teamId,
          };
          this.$store.commit("setAway", newAway);
        })
        .catch((error) => {
            console.error("Error loading roster for " + teamId + ": " + error);
            const newAway = {
              batterIds: [], 
              batterNames: [], 
              pitcherIds: [], 
              pitcherNames: [],
              score: 0,
              id: 0,
            };
            this.$store.commit("setAwayTeamName", "Select Team");
            this.$store.commit("setAway", newAway);
        });
    },
  },
  created() {
    // Fill score selection list
    this.scores.push(0);
    for (let i = 1; i <= 99; i++) {
      this.scores.push(i);
    }
  },
  computed: {
    homeTeamNames() {
      return this.$store.state.teamNames.filter(team => team !== this.awayTeamName);
    },
    awayTeamNames() {
      return this.$store.state.teamNames.filter(team => team !== this.homeTeamName);
    },
    homeTeamName: {
      get() {
        return this.$store.state.home.name;
      },
      set(name) {
        this.$store.commit("setHomeTeamName", name);
      },
    },
    homeScore: {
      get() {
        return this.$store.state.home.score;
      },
      set(score) {
        this.$store.commit("setHomeScore", score);
      },
    },
    awayTeamName: {
      get() {
        return this.$store.state.away.name;
      },
      set(name) {
        this.$store.commit("setAwayTeamName", name);
      },
    },
    awayScore: {
      get() {
        return this.$store.state.away.score;
      },
      set(score) {
        this.$store.commit("setAwayScore", score);
      },
    },
  },
};
</script>

<style>
    .score-spacer {
        margin-top: -3px;
        font-size: 30px;
    }
    .home-away {
        font-weight: bold;
        font-size: 16px;
        margin-top: -5px;
    }
</style>