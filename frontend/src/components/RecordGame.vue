<template>
      <v-card style="width: 100%; margin: 10px 10px; border: 2px solid #43A047;" 
        elevation="3"
      >
        <v-row>
          <!--Game state column-->
          <v-col cols="8" style="border-right: 2px solid #43A047;" >
            <div>
                <!--Team selection and score-->
                <v-row style="border-bottom: 2px solid #43A047;">
                  <v-col>
                    <SelectTeams/>
                  </v-col>
                </v-row>

                <!--Runners on Base/Count and Inning Row-->
                <v-row style="margin-top: 25px; margin-bottom: 3px;">
                    <!--Runners on base-->
                    <v-col cols="5" class="d-flex flex-column justify-center">
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
                    <v-col cols="7">
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
  
          <!--Input pitch column-->
          <v-col 
            cols="4" class="text-center" 
            style="margin-top: 43px; padding-right: 20px; padding-left: 0px;"
          >
            <!--Game Select-->
            <v-row>
              <v-col class="text-center">
                <v-select
                  :items="this.$store.state.seasons" 
                  v-model="season"
                  @update:modelValue="handleSeasonChange"
                  variant="solo-filled"
                  density="compact" 
                  style="margin-top: 25px; margin-left: 36px"
                  class="record-btn"
                  color="green-darken-1"
                ></v-select>
              </v-col>
            </v-row>

            <!--Start/stop game record button-->
            <v-row style="margin-top: -15px;">
              <v-col class="text-center">
                <v-btn
                    @click="handleGameButtonClick"
                    class="record-btn my-font mx-auto"
                    :color="recording ? 'red' : 'green-darken-1'"
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
              <v-col class="text-center">
                <InputPitch class="record-btn"/>
              </v-col>
            </v-row>
            
            <v-row v-else style="margin-top: 20px;">
              <v-col class="text-center">
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
        recording: false,
        innings: [],
      };
    },
    methods: {
      handleGameButtonClick() {
        console.log('Game Button clicked!');
        this.recording = !this.recording;
      },
      handleSeasonChange() {
        // Fill team selection lists
        const path = "http://" + this.$store.state.host + "/api/get_teams";
        axios.get(path)
            .then((res) => {
                const teams = res.data;
                console.log("Loaded teams: " + teams["id"].length);
                this.$store.commit("setTeamIds", teams["id"]);
                this.$store.commit("setTeamNames", teams["name"]);
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
          return this.$store.state.season;
        },
        set(newSeason) {
          this.$store.commit("setSeason", newSeason);
        },
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
</style>