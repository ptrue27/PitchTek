<template>
  <v-container fluid class="dashboard-container">

    <v-row style="margin-top: 0px">
      <v-col cols="3">

        <!--Teams-->
        <v-row>
          <v-col>
            <v-card class="text-center card-border" elevation="3">
              <v-card-title class="border-bottom">Teams</v-card-title>

              <v-row>
                <!--Select Season-->
                <v-col cols="9" class="d-flex justify-end">
                  <v-select
                    :items="seasonNames" 
                    v-model="seasonName"
                    @update:modelValue="handleSeasonChange"
                    variant="solo-filled"
                    density="compact" 
                    style="margin-top: 25px; max-width: 90%;"
                    color="green-darken-1"
                  ></v-select>
                </v-col>

                <!--Add/Delete Season-->
                <v-col cols="3" style="padding-right: 30px; padding-top: 47px;">
                  <AddSeason/> <DeleteSeason/>
                </v-col>
              </v-row>

              <v-row style="margin-top: 0px;">
                <!--Select Team-->
                <v-col cols="9" class="d-flex justify-end">
                  <v-select
                    :items="this.$store.state.account.teamNames" 
                    v-model="teamName"
                    @update:modelValue="handleTeamChange"
                    variant="solo-filled"
                    density="compact" 
                    style="max-width: 90%;"
                    color="green-darken-1"
                  ></v-select>
                </v-col>

                <!--Add/Delete Team-->
                <v-col cols="3" style="padding-right: 30px; padding-top: 21px;">
                  <AddTeam/> <DeleteTeam/>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>

        <!--Pitchers-->
        <v-row>
          <v-col>
            <v-card class="text-center card-border" elevation="3">
              <v-card-title class="border-bottom">Pitchers</v-card-title>

              <!-- Scrollable panel -->
              <v-card-text>
                <!-- Display a message if the list is empty -->
                <div v-if="pitcherNames.length === 0" style="height: 212px;">
                  <v-row style="padding-top: 77px;">
                    <v-col class="d-flex justify-center">
                      <v-card style="width: 175px;"
                          class="small-deletion-button" color="red-lighten-5"
                      >
                        <p style="padding-top: 5px; padding-bottom: 5px">
                          No pitchers available.
                        </p>
                      </v-card>
                    </v-col>
                  </v-row>
                </div>
                <!-- Display the list if it's not empty -->
                <v-list class="scroll-panel-player" v-else>
                  <v-list-item style="font-weight: bold;"
                    v-for="(pitcher, index) in pitcherNames"
                    :key="index"
                  >
                    {{ pitcher }}
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!--Batters-->
        <v-row>
          <v-col>
            <v-card class="text-center card-border" elevation="3">
              <v-card-title class="border-bottom">Batters</v-card-title>

              <!-- Scrollable panel -->
              <v-card-text>
                <!-- Display a message if the list is empty -->
                <div v-if="batterNames.length === 0" style="height: 212px;">
                  <v-row style="padding-top: 77px;">
                    <v-col class="d-flex justify-center">
                      <v-card style="width: 175px;"
                          class="small-deletion-button" color="red-lighten-5"
                      >
                        <p style="padding-top: 5px; padding-bottom: 5px">
                          No batters available.
                        </p>
                      </v-card>
                    </v-col>
                  </v-row>
                </div>
                <!-- Display the list if it's not empty -->
                <v-list class="scroll-panel-player" v-else>
                  <v-list-item style="font-weight: bold;"
                    v-for="(batter, index) in batterNames"
                    :key="index"
                  >
                    {{ batter }}
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
              <v-col cols="8" class="d-flex justify-center">
                <v-select
                  :items="this.$store.state.account.gameNames" 
                  v-model="gameName"
                  @update:modelValue="handleGameChange"
                  variant="solo-filled"
                  density="compact" 
                  style="margin-top: 25px; max-width: 350px;"
                  color="green-darken-1"
                ></v-select>
              </v-col>
              <v-col cols="4" class="d-flex justify-start">
                <v-btn text="Current Game"
                  style="margin-top: 25px;"
                  variant="outlined"
                  color="green-darken-1"
                  @click="handleCurrentGameClick"
                />
              </v-col>
            </v-row>

            <v-row style="padding-right: 10px; border-top: #43A047 2px solid;">
              <v-col style="padding-top: 0px;">
                <!--Empty message-->        
                <div v-if="gameStates.length === 0" 
                  class="empty-list-message" style="height: 658px;"
                >
                  <v-row style="padding-top: 250px;">
                    <v-col class="d-flex justify-center">
                      <v-card style="width: 175px; "
                          class="small-deletion-button" color="red-lighten-5"
                      >
                        <p style="padding-top: 5px; padding-bottom: 5px">
                          No pitches available.
                        </p>
                      </v-card>
                    </v-col>
                  </v-row>
                </div>

                <!--Gamestates list-->
                <v-list v-else class="scroll-panel-prediction">
                  <v-list-item v-for="(gameState, index) in gameStates" 
                    :key="index" 
                    class="component"
                  >
                    <my-custom-component :storeSnapshot="gameStates[index]" />
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
          </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
  
<script>
  import MyCustomComponent from '@/components/PreviousPrediction.vue';
  import AddSeason from '@/components/AddSeason.vue'
  import DeleteSeason from '@/components/DeleteSeason.vue'
  import AddTeam from '@/components/AddTeam.vue'
  import DeleteTeam from '@/components/DeleteTeam.vue'
  import {mapState} from 'vuex';
  import axios from 'axios';
  
  export default {
    components: {
      MyCustomComponent,
      AddSeason,
      DeleteSeason,
      AddTeam,
      DeleteTeam,
    },
    data() {
      return {
        components_two: [{
          inning: "1∧",
          home_name: "San Francisco Giants",
          home_score: 7,
          away_name: "Los Angeles Dodgers",
          away_score: 2,
          prediction_img: "default_heat_map.jpg",
          prediction_speed: 88.9,
          prediction_location: 4,
          prediction_confidence: 67.45,
          prediction_type: "Slider (SL)",
          outs: 1,
          balls: 2,
          strikes: 2,
          base_first: true,
          base_second: false,
          base_third: true,
          pitcher_name: "Logan Webb",
          pitcher_img: "",
          batter_name: "Mookie Betts",
          batter_img: "",
        },{
          inning: "1∧",
          home_name: "San Francisco Giants",
          home_score: 7,
          away_name: "Los Angeles Dodgers",
          away_score: 2,
          prediction_img: "default_heat_map.jpg",
          prediction_speed: 88.9,
          prediction_location: 4,
          prediction_confidence: 67.45,
          prediction_type: "Slider (SL)",
          outs: 1,
          balls: 2,
          strikes: 2,
          base_first: true,
          base_second: false,
          base_third: true,
          pitcher_name: "Logan Webb",
          pitcher_img: "",
          batter_name: "Mookie Betts",
          batter_img: "",
        },{
          inning: "1∧",
          home_name: "San Francisco Giants",
          home_score: 7,
          away_name: "Los Angeles Dodgers",
          away_score: 2,
          prediction_img: "default_heat_map.jpg",
          prediction_speed: 88.9,
          prediction_location: 4,
          prediction_confidence: 67.45,
          prediction_type: "Slider (SL)",
          outs: 1,
          balls: 2,
          strikes: 2,
          base_first: true,
          base_second: false,
          base_third: true,
          pitcher_name: "Logan Webb",
          pitcher_img: "",
          batter_name: "Mookie Betts",
          batter_img: "",
        }],
      };
    },
    methods: {
      handleGameChange() {
        const index = this.$store.state.account.gameNames.indexOf(this.gameName);
        const gameId = this.$store.state.account.gameIds[index];
        const path = "http://" + this.$store.state.host + "/api/get_history";
        const params = { 
          game_id: gameId,
        };

        axios.get(path, { params })
            .then((res) => {
                const gameStates = res.data.game_states;
                console.log("Loaded game states: " + gameStates.length);
                this.$store.commit("setAccountGameStates", gameStates);
            })
            .catch((error) => {
                console.error("Error loading game: " + error);
            });
      },
      handleCurrentGameClick() {
        this.$store.commit("setAccountGameStates", this.$store.state.gameStates);
        this.$store.commit("setAccountGame", "Current");
      },
      handleSeasonChange() {
        // Fill team selection list
        var path = "http://" + this.$store.state.host + "/api/get_teams";
        var params = { 
          season_id: this.$store.state.account.seasonId,
          season_name: this.seasonName,
        };

        axios.get(path, { params })
            .then((res) => {
                const teams = res.data;
                console.log("Loaded teams: " + teams["ids"].length);
                this.$store.commit("setAccountTeams", teams);
            })
            .catch((error) => {
                console.error("Error loading teams: " + error);
            });

        // Fill game selection list
        path = "http://" + this.$store.state.host + "/api/get_games";
        params = { 
          season_id: this.$store.state.account.seasonId,
        };

        axios.get(path, { params })
            .then((res) => {
                let games = res.data;
                console.log("Loaded games: " + games.ids.length);
                this.$store.commit("setAccountGames", games);
            })
            .catch((error) => {
                console.error("Error loading teams: " + error);
            });
      },
      handleTeamChange() {
        const index = this.$store.state.account.teamNames.indexOf(this.teamName);
        const teamId = this.$store.state.account.teamIds[index];
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
            this.$store.commit("setAccountRoster", roster);
          })
          .catch((error) => {
              console.error("Error loading roster for " + teamId + ": " + error);
          });
      },
    },
    computed: {
      ...mapState(['inning', 'home', 'away',
        'prediction', 'outs', 'balls', 'strikes', 'bases', 'current']),
      seasonNames() {
        return this.$store.state.season.names;
      },
      pitcherNames() {
        return this.$store.state.account.pitcherNames; 
      },
      batterNames() {
        return this.$store.state.account.batterNames; 
      },
      gameStates() {
        return this.$store.state.account.gameStates; 
      },
      seasonName: {
        get() {
          return this.$store.state.account.seasonName;
        },
        set(newName) {
          this.$store.commit("setAccountSeason", newName);
        },
      },
      teamName: {
        get() {
          return this.$store.state.account.teamName;
        },
        set(newName) {
          this.$store.commit("setAccountTeam", newName);
        },
      },
      gameName: {
        get() {
          return this.$store.state.account.gameName;
        },
        set(newName) {
          this.$store.commit("setAccountGame", newName);
        },
      },
    }
  };
</script>
  
<style>
.scroll-panel-player {
  height: 200px;
  overflow-y: auto;
}
.scroll-panel-prediction {
  height: 646px;
  overflow-y: auto;
}
</style>