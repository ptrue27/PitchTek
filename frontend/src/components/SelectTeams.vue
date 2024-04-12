<template>
    <!--Team selection-->
    <v-row class="text-center" style="margin-bottom: -40px;">
        <!--Input home team-->
        <v-col cols="6">
            <v-select
                :items="homeTeamNames" 
                v-model="home.teamName"
                @update:modelValue="handleHomeTeamChange"
                variant="filled" 
                density="compact"
            ></v-select>
        </v-col>
                  
        <!--Input away team-->
        <v-col cols="6">
            <v-select
                :items="awayTeamNames" 
                v-model="away.teamName"
                @update:modelValue="handleAwayTeamChange"
                variant="filled" 
                density="compact"
            ></v-select>
        </v-col>
     </v-row>
              
    <!--Score input-->
    <v-row>
        <!--Home Score-->
        <v-col cols="3" style="margin-top: 10px;" align="right">
            <p class="home-away" style="margin-right: 10px;">
                Home
            </p>
        </v-col>
        <v-col cols="2">
            <v-select
                :items="scores"
                v-model="home.score"
                density="compact"
                variant="solo-filled"
            ></v-select>
        </v-col>

        <v-col cols="2" class="score-spacer text-center">
            <p>-</p>
        </v-col>
        
        <!--Away Score-->
        <v-col cols="2">
            <v-select
                :items="scores"
                v-model="away.score"
                density="compact"
                variant="solo-filled"
            ></v-select>
        </v-col>
        <v-col cols="3" style="margin-top: 10px;" align="left">
            <p class="home-away" style="margin-left: 10px;">
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
        teamIds: [],
        teamNames: [],
        scores: [],
        home: {
            teamName: "Select Team",
            score: 0,
        },
        away: {
            teamName: "Select Team",
            score: 0,
        },
    };
  },
  methods: {
    handleHomeTeamChange() {
      const index = this.teamNames.indexOf(this.home.teamName);
      const teamId = this.teamIds[index];
      const path = 'http://localhost:5000/api/get_roster/' + teamId;

      axios.get(path)
        .then((res) => {
          const roster = res.data;
          console.log("Loaded roster for " + teamId + ": " + 
            roster.batters.id.length + " batters, " +
            roster.pitchers.id.length + " pitchers"
          );
          const newHome = {
            batterIds: roster.batters.id, 
            batterNames: roster.batters.name,
            pitcherIds: roster.pitchers.id,
            pitcherNames: roster.pitchers.name,
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
            };
            this.$store.commit("setHome", newHome);
        });
    },
    handleAwayTeamChange() {
      const index = this.teamNames.indexOf(this.away.teamName);
      const teamId = this.teamIds[index];
      const path = 'http://localhost:5000/api/get_roster/' + teamId;

      axios.get(path)
        .then((res) => {
          const roster = res.data;
          console.log("Loaded roster for " + teamId + ": " + 
            roster.batters.id.length + " batters, " +
            roster.pitchers.id.length + " pitchers"
          );
          const newAway = {
            batterIds: roster.batters.id, 
            batterNames: roster.batters.name,
            pitcherIds: roster.pitchers.id,
            pitcherNames: roster.pitchers.name,
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
            };
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

    // Fill team selection lists
    const path = "http://localhost:5000/api/get_teams";
    axios.get(path)
        .then((res) => {
            const teams = res.data;
            console.log("Loaded teams: " + teams["id"].length)
            this.teamIds = teams["id"]
            this.teamNames = teams["name"];
        })
        .catch((error) => {
            console.error("Error loading teams: " + error);
        });
  },
  computed: {
    homeTeamNames() {
      return this.teamNames.filter(team => team !== this.away.teamName);
    },
    awayTeamNames() {
      return this.teamNames.filter(team => team !== this.home.teamName);
    },
  }
};
</script>

<style>
    .score-spacer {
        margin-top: -3px;
        font-size: 30px;
    }
    .home-away {
        font-weight: bold;
        font-size: 20px;
        margin-top: -5px;
    }
</style>