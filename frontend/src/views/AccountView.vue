<template>
  <v-container fluid class="dashboard-container">
    <!--Manage PitchTek Data-->
    <v-row>
      <v-col cols="4" />
      <v-col cols="4" class="text-center" style="margin-top: 20px;">
        <h2 style="text-decoration: underline;">Manage PitchTek Data</h2>
      </v-col>
      <v-col cols="4" class="d-flex justify-end">
        <v-btn>Logout</v-btn>
      </v-col>
    </v-row>

    <v-row style="margin-top: 0px">
      <v-col cols="3">

        <!--Manage Teams-->
        <v-row>
          <v-col>
            <v-card class="text-center card-border" elevation="3">
              <v-card-title class="border-bottom">Teams</v-card-title>

              <!--Season Select-->
              <v-row>
                <v-col cols="12" class="d-flex justify-center">
                  <v-select
                    :items="this.$store.state.season.names" 
                    v-model="seasonName"
                    @update:modelValue="handleSeasonChange"
                    variant="solo-filled"
                    density="compact" 
                    style="margin-top: 25px; max-width: 80%;"
                    color="green-darken-1"
                  ></v-select>
                </v-col>
              </v-row>

              <!--Team Select-->
              <v-row>
                <v-col cols="12" class="d-flex justify-center">
                  <v-select
                    :items="this.$store.state.manage.teamNames" 
                    v-model="teamName"
                    @update:modelValue="handleTeamChange"
                    variant="solo-filled"
                    density="compact" 
                    style="max-width: 80%;"
                    color="green-darken-1"
                  ></v-select>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>

        <!--Pitchers-->
        <v-row>
          <v-col>
            <v-card class="text-center" elevation="3">
              <v-card-title class="border-bottom">Pitchers</v-card-title>

              <!-- Fixed-size scrollable panel -->
              <v-card-text>
                <v-list class="scroll-panel">
                  <v-list-item style="font-weight: bold;"
                    v-for="(pitcher, index) in this.$store.state.manage.pitcherNames"
                    :key="index"
                  >
                    {{ pitcher }}
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

      </v-col>

      <v-col cols="9">
          <v-card class="text-center card-border">
            <v-card-title class="border-bottom">
              Prediction History
            </v-card-title>

            <!--Game Select-->
            <v-row>
              <v-col cols="12" class="d-flex justify-center">
                <v-select
                  :items="this.$store.state.manage.gameNames" 
                  v-model="gameName"
                  @update:modelValue="handleGameChange"
                  variant="solo-filled"
                  density="compact" 
                  style="margin-top: 25px; max-width: 350px;"
                  color="green-darken-1"
                ></v-select>
              </v-col>
            </v-row>

            <v-row>
              <v-col>
                <div v-for="(componentData, index) in components" :key="index" class="component">
                  <!-- Pass the store snapshot as a prop to my-custom-component -->
                  <my-custom-component :storeSnapshot="componentData" />
                </div>
              </v-col>
            </v-row>
          </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
  
<script>
  import MyCustomComponent from '@/components/PreviousPrediction.vue';
  import {mapState} from 'vuex';
  import axios from 'axios';
  
  export default {
    components: {
      MyCustomComponent
    },
    data() {
      return {
        components: [],
      };
    },
    methods: {
      handleGameChange() {
        const index = this.$store.state.manage.gameNames.indexOf(this.gameName);
        const gameId = this.$store.state.manage.gameIds[index];
        const path = "http://" + this.$store.state.host + "/api/get_history";
        const params = { 
          game_id: gameId,
        };

        axios.get(path, { params })
            .then((res) => {
                const gameStates = res.data.game_states;
                console.log("Loaded game states: " + gameStates.length);
                this.$store.commit("setManagerGameStates", gameStates);
            })
            .catch((error) => {
                console.error("Error loading game: " + error);
            });
      },
      handleSeasonChange() {
        // Fill team selection list
        const index = this.$store.state.season.names.indexOf(this.seasonName);
        const seasonId = this.$store.state.season.ids[index];
        var path = "http://" + this.$store.state.host + "/api/get_teams";
        var params = { 
          season_id: seasonId,
          season_name: this.seasonName,
        };

        axios.get(path, { params })
            .then((res) => {
                const teams = res.data;
                console.log("Loaded teams: " + teams["ids"].length);
                this.$store.commit("setManagerTeams", teams);
            })
            .catch((error) => {
                console.error("Error loading teams: " + error);
            });

        // Fill game selection list
        path = "http://" + this.$store.state.host + "/api/get_games";
        params = { 
          season_id: seasonId,
        };

        axios.get(path, { params })
            .then((res) => {
                const games = res.data;
                console.log("Loaded games: " + games.ids.length);
                this.$store.commit("setManagerGames", games);
            })
            .catch((error) => {
                console.error("Error loading teams: " + error);
            });
      },
      handleTeamChange() {
        const index = this.$store.state.manage.teamNames.indexOf(this.teamName);
        const teamId = this.$store.state.manage.teamIds[index];
        const path = 'http://' + this.$store.state.host + '/api/get_roster';
        const params = {
          season_name: this.seasonName,
          team_id: teamId,
        };

        axios.get(path, { params })
          .then((res) => {
            const roster = res.data;
            console.log("Loaded roster for " + teamId + ": " + 
              roster.batters.ids.length + " batters, " +
              roster.pitchers.ids.length + " pitchers"
            );
            this.$store.commit("setManagerRoster", roster);
          })
          .catch((error) => {
              console.error("Error loading roster for " + teamId + ": " + error);
          });
      },
      addComponent() {
        // Capture the entire state of the Vuex store
        const storeSnapshot = {
          inning: this.inning,
          home_name: this.home.name,
          home_score: this.home.score,
          away_name: this.away.name,
          away_score: this.away.score,
          prediction_img: this.prediction.img,
          prediction_speed: this.prediction.speed,
          prediction_location: this.prediction.location,
          prediction_confidence: this.prediction.confidence,
          prediction_type: this.prediction.type,
          outs: this.outs,
          balls: this.balls,
          strikes: this.strikes,
          base_first: this.bases[0],
          base_second: this.bases[1],
          base_third: this.bases[2],
          pitcher_name: this.current.pitcher.name,
          pitcher_img: this.current.pitcher.img,
          batter_name: this.current.batter.name,
          batter_img: this.current.batter.img,
        };
        // Push the store snapshot into components array
        this.components.unshift(storeSnapshot);
      }
    },
    created() {
      this.emitter.on('UpdateHistory', this.addComponent);
    },
    computed: {
      ...mapState(['inning', 'home', 'away',
        'prediction', 'outs', 'balls', 'strikes', 'bases', 'current']),
      seasonName: {
        get() {
          return this.$store.state.manage.seasonName;
        },
        set(newName) {
          this.$store.commit("setManageSeason", newName);
        },
      },
      teamName: {
        get() {
          return this.$store.state.manage.teamName;
        },
        set(newName) {
          this.$store.commit("setManageTeam", newName);
        },
      },
      gameName: {
        get() {
          return this.$store.state.manage.gameName;
        },
        set(newName) {
          this.$store.commit("setManageGame", newName);
        },
      },
    }
  };
</script>
  
<style>
.scroll-panel {
  height: 200px;
  overflow-y: auto;
}
</style>