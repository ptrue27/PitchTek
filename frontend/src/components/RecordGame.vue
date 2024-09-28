<template>
      <v-card style="width: 100%; margin: 10px 10px;" 
        elevation="3" class="card-border"
      >
        <v-row>
          <!--Input pitch column-->
          <v-col 
            cols="4" class="text-center" style="padding-left: 18px;"
          >
            <!--Title-->
            <v-row class="border-bottom" style="margin-top: 0px; font-weight: bold">
                <v-col class="text-center">
                    <div>Record Game</div>
                </v-col>
            </v-row>

            <!--Season Select-->
            <v-row>
              <v-col cols="12" class="d-flex justify-center">
                <v-select
                  :items="this.$store.state.season.names" 
                  v-model="season"
                  @update:modelValue="handleSeasonChange"
                  variant="solo-filled"
                  density="compact" 
                  style="margin-top: 25px; max-width: 225px"
                  class="record-btn"
                  color="green-darken-1"
                  :disabled="this.$store.state.recording"
                ></v-select>
              </v-col>
            </v-row>

            <!--Start/stop game record button-->
            <v-row style="margin-top: -15px;">
              <v-col cols="12" class="d-flex justify-center">
                <v-btn
                    @click="handleGameButtonClick"
                    class="record-btn my-font mx-auto"
                    :color="recording ? 'red' : 'green-darken-1'"
                    :disabled="isButtonDisabled"
                >
                  <template v-if="recording">
                      <v-icon left>mdi-stop-circle</v-icon>
                      <p style="margin-left: 8px;">Stop Game</p>
                  </template>
                  <template v-else>
                      <v-icon left>mdi-play-circle</v-icon>
                      <p style="margin-left: 8px;">Start Game</p>
                  </template>
                </v-btn>
              </v-col>
            </v-row>
            
            <!--Input pitch dialog-->
            <v-row v-if="recording" style="margin-top: 20px;">
              <v-col cols="12" class="d-flex justify-center">
                <InputPitch class="record-btn"/>
              </v-col>
            </v-row>
            
            <v-row v-else style="margin-top: 20px;">
              <v-col cols="12" class="d-flex justify-center">
                <v-btn 
                    class="record-btn"
                    @click="this.$store.commit('resetDashboard')"
                    prepend-icon="mdi-refresh"
                    text="Reset"
                    color="green-darken-1"
                    variant="outlined"
                ></v-btn>
              </v-col>
            </v-row>

          </v-col>

          <!--Game state column-->
          <v-col cols="8" 
            style="border-left: 2px solid #43A047; margin-top: 5px; margin-bottom: 1px">
            <div>
                <!--Team selection and score-->
                <v-row>
                  <v-col>
                    <SelectTeams/>
                  </v-col>
                </v-row>

                <!--Runners on Base/Count and Inning Row-->
                <v-row style="margin-top: 25px; margin-bottom: 3px;">
                    <!--Runners on base-->
                    <v-col cols="4" class="d-flex flex-column justify-center">
                      <v-div>
                        <v-row class="no-wrap my-font text-center">
                          <v-col style="padding-bottom: 0;">
                            <p>On Base</p>
                          </v-col>
                        </v-row>
                        <!--Second base-->
                        <v-row class="no-wrap">
                          <v-col class="text-center">
                            <v-chip
                              @click="this.$store.commit('toggleBase', 1)"
                              :style="{backgroundColor: getBaseColor(1)}" 
                              class="square-chip" size="small"
                            >2</v-chip>
                          </v-col>
                        </v-row>

                        <!--First and third base-->
                        <v-row class="mt-0">
                          <v-spacer></v-spacer>
                          <v-col class="text-center">
                            <v-chip
                              @click="this.$store.commit('toggleBase', 2)"
                              :style="{backgroundColor: getBaseColor(2)}" 
                              class="square-chip" size="small"
                            >3</v-chip>
                          </v-col>
                          <v-col class="text-center">
                            <v-chip
                              @click="this.$store.commit('toggleBase', 0)"
                              :style="{backgroundColor: getBaseColor(0)}" 
                              class="square-chip" size="small"
                            >1</v-chip>
                          </v-col>
                          <v-spacer></v-spacer>
                        </v-row>

                        <!--Homeplate-->
                        <v-row class="mt-0">
                          <v-col class="text-center">
                            <v-img 
                              src="@/assets/homeplate.png"
                              height="25px"
                              >
                            </v-img>
                          </v-col>
                        </v-row>

                      </v-div>
                    </v-col>

                    <!--Innings and count-->
                    <v-col cols="8" style="padding-right: 20px;">
                      <!--Inning-->
                      <v-row style="margin-bottom: 2px;">
                        <v-col align="right" cols="4" class="no-wrap my-font">
                          <p class="inning-text" style="font-weight: bold;">
                            Inning
                          </p>
                        </v-col>
                        <v-col>
                          <v-select
                            :items="innings" 
                            v-model="inning"
                            variant="solo-filled"
                            density="compact" 
                            class="inning-v-select"
                            color="green-darken-1"
                          ></v-select>
                        </v-col>
                      </v-row>

                      <!--Outs-->
                      <v-row no-gutters class="no-wrap mt-0">
                        <v-col align="right" cols="4">
                          <p class="out-ball-strike-text my-font">
                            Outs
                          </p>
                        </v-col>
                        <v-col v-for="(_, index) in 3" :key="index" cols="2">
                          <v-chip 
                            @click="this.$store.commit('setOuts', index)" 
                            :style="{backgroundColor: getColor(
                              this.$store.state.outs, index)}" 
                            size="x-small" class="mr-1"
                          >
                            {{ index }}
                          </v-chip>
                        </v-col>
                      </v-row>
                      
                      <!--Balls-->
                      <v-row no-gutters class="no-wrap mt-2">
                        <v-col align="right" cols="4" class="my-font">
                          <p class="out-ball-strike-text">
                            Balls
                          </p>
                        </v-col>
                        <v-col v-for="(_, index) in 4" :key="index" cols="2">
                          <v-chip 
                            @click="this.$store.commit('setBalls', index)" 
                            :style="{backgroundColor: getColor(
                              this.$store.state.balls, index)}" 
                            size="x-small" class="mr-1"
                          >
                            {{ index }}
                          </v-chip>
                        </v-col>
                      </v-row>

                      <!--Strikes-->
                      <v-row no-gutters class="no-wrap mt-2">
                        <v-col align="right" cols="4" class="my-font">
                          <p class="out-ball-strike-text">
                            Strikes
                          </p>
                        </v-col>
                        <v-col v-for="(_, index) in 3" :key="index" cols="2">
                          <v-chip 
                            @click="this.$store.commit('setStrikes', index)"  
                            :style="{backgroundColor: getColor(
                              this.$store.state.strikes, index)}" 
                            size="x-small" class="mr-1"
                          >
                            {{ index }}
                          </v-chip>
                        </v-col>
                      </v-row>

                    </v-col>
                </v-row>
              </div>
          </v-col>
  
        </v-row>
      </v-card>
</template>

<script>
  import InputPitch from "@/components/InputPitch.vue";
  import SelectTeams from "@/components/SelectTeams.vue";
  import axios from "axios";

  export default {
    components: {
      InputPitch,
      SelectTeams,
    },
    data() {
      return {
        innings: [],
      };
    },
    methods: {
      handleGameButtonClick() {
        this.recording = !this.recording;
        if (!this.recording) {
          console.log("Stopped game")
        } 
        else {
          const path = "http://" + this.$store.state.host + "/api/new_game";
          const token = localStorage.getItem("token");
          const body = {
            home_team_name: this.$store.state.home.name,
            away_team_name: this.$store.state.away.name,
            season_id: this.$store.state.season.id,
          };
          console.log(this.$store.state.season);

          axios.post(path, body, { headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    } 
          })
              .then((res) => {
                  const gameId = res.data.id;
                  console.log("Started game: " + gameId);
                  this.$store.commit("setGameId", gameId);
              })
              .catch((error) => {
                  console.error("Error starting game: " + error);
                  this.recording = !this.recording;
              });
        }
      },
      handleSeasonChange() {
        // Set season id
        const index = this.$store.state.season.names.indexOf(this.season);
        const seasonId = this.$store.state.season.ids[index];
        this.$store.commit("setSeasonId", seasonId);
        console.log("Set season: " + this.$store.state.season.id);

        // Fill team selection lists
        const path = "http://" + this.$store.state.host + "/api/get_teams";
        const token = localStorage.getItem("token");
        const params = { 
          season_id: this.$store.state.season.id,
          season_name: this.$store.state.season.name,
        };
        axios.get(path, params, { headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    } 
        })
            .then((res) => {
                const teams = res.data;
                console.log("Loaded teams: " + teams["ids"].length);
                this.$store.commit("setTeamIds", teams["ids"]);
                this.$store.commit("setTeamNames", teams["names"]);
            })
            .catch((error) => {
                console.error("Error loading teams: " + error);
            });
      },
      getColor(state, index) {
        if(state==index) {
          if(index==0){
            return 'gray';
          } else {
            return '#43A047';
          }
        } else {
          return '#EEEEEE';
        }
      },
      getBaseColor(index) {
        if(this.$store.state.bases[index]) {
          return '#43A047';
        } else {
          return '#EEEEEE';
        }
      },
    },
    created() {
      // Fill inning selection list
      for (let i = 1; i <= 99; i++) {
        this.innings.push(`${i}∧`, `${i}∨`);
      }
    },
    computed: {
      inning: {
        get() {
          return this.$store.state.inning;
        },
        set(newInning) {
          this.$store.commit("setInning", newInning);
        },
      },
      season: {
        get() {
          return this.$store.state.season.name;
        },
        set(seasonName) {
          this.$store.commit("setSeasonName", seasonName);
        },
      },
      recording: {
        get() {
          return this.$store.state.recording;
        },
        set(newState) {
          this.$store.commit("setRecording", newState);
        },
      },
      isButtonDisabled() {
          return (!this.recording && 
            ((this.$store.state.away.id == 0) || (this.$store.state.home.id == 0)));
      },
    }
  };
</script>
  
<style>
  .inning-v-select {
    margin-top: -10px;
    margin-bottom: -25px;
    max-width: 90px;
    margin-left: -5px;
  }
  .my-font {
    font-size: 14px;
    font-weight: bold;
  }
  .record-btn {
    width: 75%;
    min-width: 90px;
  }
  .square-chip {
    width: 25px;
    height: 25px;
    border-radius: 3px;
    border: 2px solid rgb(64, 64, 64);
    justify-content: center;
  }
  .inning-text {
    margin-top: 3px;
    margin-right: 3px;
  }
  .out-ball-strike-text {
    margin-top: 3px;
    margin-right: 20px;
  }
  .card-border {
    border: 2px solid #43A047;
  }
</style>