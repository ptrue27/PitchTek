<template>
    <v-container fluid>
      <v-card>
        <v-row>
          <!--Game state column-->
          <v-col cols="8">
            <v-container fluid>
                <v-row class="text-center" style="margin-bottom: -40px;">
                    <!--Input home team-->
                    <v-col cols="6">
                      <v-select
                        :items="homeTeamNames" 
                        v-model="home.teamName"
                        @update:modelValue="handleHomeTeamChange"
                        variant="filled" 
                        density="compact"
                        class="my-label team-name"
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
                          class="my-label team-name"
                        ></v-select>
                    </v-col>
                </v-row>
                
                <!--Score input-->
                <v-row class="score-row">
                          <!--Home Score and "-"-->
                          <v-col cols="3" style="margin-top: 10px;" align="right">
                            <p style="margin-right: 10px;">Home</p>
                          </v-col>
                          <v-col cols="2">
                                <v-select
                                  :items="scores"
                                  v-model="home.score"
                                  density="compact"
                                  variant="solo-filled"
                                ></v-select>
                          </v-col>
                          <v-col 
                            cols="2"
                            style="margin-top: -2px; margin-left: -10px; margin-right: -10px;"
                            class="score-spacer text-center"
                          >
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
                            <p style="margin-left: 10px;">Away</p>
                          </v-col>
                </v-row>


                <!--Count and Inning Row-->
                <v-row>
                    <!--Runners on base-->
                    <v-col cols="5" class="d-flex flex-column justify-center">
                      <v-div>
                        <v-row class="no-wrap my-font text-center">
                          <v-col style="padding-bottom: 0;">On Base</v-col>
                        </v-row>
                        <!--Second base-->
                        <v-row class="no-wrap">
                          <v-col class="text-center">
                            <v-chip
                              @click="toggleBase(2)"
                              :style="{backgroundColor: baseColors[1]}" 
                              class="square-chip" size="small"
                            >2</v-chip>
                          </v-col>
                        </v-row>

                        <!--First and third base-->
                        <v-row class="mt-0">
                          <v-spacer></v-spacer>
                          <v-col class="text-center">
                            <v-chip
                              @click="toggleBase(3)"
                              :style="{backgroundColor: baseColors[2]}" 
                              class="square-chip" size="small"
                            >3</v-chip>
                          </v-col>
                          <v-col class="text-center">
                            <v-chip
                              @click="toggleBase(1)"
                              :style="{backgroundColor: baseColors[0]}" 
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
                      <v-row style="margin-bottom: 0px;">
                        <v-col align="right" cols="4" class="no-wrap my-font">
                          <p class="inning-text"> Inning</p>
                        </v-col>
                        <v-col>
                          <v-select
                            :items="innings" 
                            v-model="inning"
                            @update:modelValue="handleInningChange"
                            variant="solo-filled"
                            density="compact" 
                            class="inning-v-select"
                          ></v-select>
                        </v-col>
                      </v-row>

                      <!--Outs-->
                      <v-row no-gutters class="no-wrap mt-0">
                        <v-col align="right" cols="4" class="my-font">
                          <p class="out-ball-strike-text"> Outs</p>
                        </v-col>
                        <v-col cols="2">
                          <v-chip 
                            @click="setOuts(0)" 
                            :style="{backgroundColor: outColors[0]}" 
                            size="x-small" class="mr-1"
                          >0</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip 
                            @click="setOuts(1)" 
                            :style="{backgroundColor: outColors[1]}"
                            size="x-small" class="mr-1"
                          >1</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip
                              @click="setOuts(2)" 
                              :style="{backgroundColor: outColors[2]}"
                              size="x-small" class="mr-1"
                          >2</v-chip>
                        </v-col>
                      </v-row>
                      
                      <!--Balls-->
                      <v-row no-gutters class="no-wrap mt-2">
                        <v-col align="right" cols="4" class="my-font">
                          <p class="out-ball-strike-text">Balls</p>
                        </v-col>
                        <v-col cols="2">
                          <v-chip 
                            @click="setBalls(0)" 
                            :style="{backgroundColor: ballColors[0]}"
                            size="x-small" class="mr-1"
                          >0</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip 
                            @click="setBalls(1)" 
                            :style="{backgroundColor: ballColors[1]}"
                            size="x-small" class="mr-1"
                          >1</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip 
                            @click="setBalls(2)" 
                            :style="{backgroundColor: ballColors[2]}"
                            size="x-small" class="mr-1"
                          >2</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip 
                            @click="setBalls(3)" 
                            :style="{backgroundColor: ballColors[3]}"
                            size="x-small" class="mr-1"
                          >3</v-chip>
                        </v-col>
                      </v-row>

                      <!--Strikes-->
                      <v-row no-gutters class="no-wrap mt-2">
                        <v-col align="right" cols="4" class="my-font">
                          <p class="out-ball-strike-text">Strikes</p>
                        </v-col>
                        <v-col cols="2">
                          <v-chip 
                            @click="setStrikes(0)" 
                            :style="{backgroundColor: strikeColors[0]}"
                            size="x-small" class="mr-1"
                          >0</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip 
                            @click="setStrikes(1)" 
                            :style="{backgroundColor: strikeColors[1]}"
                            size="x-small" class="mr-1"
                          >1</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip 
                            @click="setStrikes(2)" 
                            :style="{backgroundColor: strikeColors[2]}"
                            size="x-small" class="mr-1"
                          >2</v-chip>
                        </v-col>
                      </v-row>

                    </v-col>
                </v-row>
            </v-container>
          </v-col>
  
          <!--Input pitch column-->
          <v-col cols="4" class="d-flex flex-column justify-center pr-5">
              <!--Input pitch dialog-->
              <div>
                  <v-dialog width="500">
                      <template v-slot:activator="{ props }">
                          <v-img
                              src="@/assets/strikezone.png"
                              v-bind="props"
                              class="input-pitch-v-dialog mx-auto"
                          ></v-img>
                      </template>

                      <template v-slot:default="{ isActive }">
                          <v-card title="Input Pitch">
                            <v-card-text>
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                            </v-card-text>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn
                                    text="Close"
                                    @click="isActive.value = false"
                                ></v-btn>
                            </v-card-actions>
                          </v-card>
                      </template>
                  </v-dialog>
              </div>

              <!--Predict button-->
              <v-btn
                  prepend-icon="mdi-arrow-right-bold-box"
                  class="predict-btn my-font mx-auto"
                  @click="handlePredictButtonClick"
              >Predict</v-btn>   

              <!--Start/stop game record button-->
              <v-btn
                  prepend-icon="mdi-record-circle"
                  @click="handleGameButtonClick"
                  class="start-stop-game-btn my-font mx-auto"
              >Start<br>Game</v-btn>

          </v-col>
        </v-row>
      </v-card>
    </v-container>
</template>
  
<style>
  .inning-v-select {
    margin-top: -10px;
    margin-bottom: -25px;
    max-width: 90px;
    margin-left: -5px;
  }
  .score-v-text-field {
    margin-top: -37px;
    min-width: 0;
    max-width: 75px;
    padding: 0;
  }
  .my-label label {
    font-size: 12px;
    text-align: center;
  }
  .team-name {
    font-size: 20px;
  }
  .my-font {
    font-size: 12px;
  }
  .score-spacer {
    margin-top: -37px;
    font-size: 30px;
  }
  .no-wrap {
    white-space: nowrap;
  }
  .input-pitch-v-dialog {
    width: 95%;
    max-height: 175px;
    margin-top: 2px;
    margin-bottom: 5px;
  }
  .start-stop-game-btn {
    width: 75%;
    min-width: 90px;
    margin-top: 5px;
    margin-bottom: 5px;
  }
  .predict-btn {
    min-width: 90px;
    width: 75%;
    margin-top: 5px;
    margin-bottom: 2px;
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

<script>
  import axios from 'axios';

  export default {
    data() {
      return {
        curr_pitcher_id: "NA",
        unsetColor: 'white',
        setBaseColor: 'cadetblue',
        set0Color: 'gray',
        setColor: 'cadetblue',

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


        onBase: [false, false, false],
        baseColors: [],
        innings: [],
        inning: "1∧",
        outNumber: 0,
        outColors: [],
        ballNumber: 0,
        ballColors: [],
        strikeNumber: 0,
        strikeColors: [],
      };
    },
    methods: {
      handleInningChange() {
        this.$store.commit("setInning", this.inning);
      },
      handleHomeTeamChange() {
        const index = this.teamNames.indexOf(this.home.teamName);
        const teamId = this.teamIds[index];
        const path = 'http://localhost:5000/get_roster/' + teamId;

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
        const path = 'http://localhost:5000/get_roster/' + teamId;

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
      handleGameButtonClick() {
        console.log('Game Button clicked!');
        // Start or stop game recording
      },
      handlePredictButtonClick() {
        console.log('Predict Button clicked!');

        const path = 'http://localhost:5000/make_prediction';

        axios.get(path, {params: { param1: this.gameState, param2: this.curr_pitcher_id}})
          .then((res) => {
            console.log("Pitch Prediction Recieved for pitcher " + this.curr_pitcher_id + ": " + res.data)

            let eventObject = {
                HomeTeamName: this.home.teamName,
                HomeScore: this.home.score,
                AwayTeamName: this.away.teamName,
                AwayScore: this.away.score,
                Inning: this.inning,
                pitchType: res.data[0],
                pitcherId: this.curr_pitcher_id,
                baseColors: this.baseColors,
            };

            this.emitter.emit("UpdateHistory", eventObject);
            this.emitter.emit("ChangePitch", res.data)

          })
          .catch((error) => {
            console.error(error);
          });
      },
      toggleBase(baseNumber) {
        console.log('Toggled base:', baseNumber);
        const i = baseNumber - 1;
        this.onBase[i] = !this.onBase[i];
        if(!this.onBase[i]){
          this.baseColors[i] = this.unsetColor;
        }
        else{
          this.baseColors[i] = this.setBaseColor;
        }
      },
      setOuts(outNumber) {
        this.outNumber = outNumber;
        console.log('Changed number of outs:', outNumber)
        if(outNumber == 0) {
          this.outColors = [this.set0Color, this.unsetColor, this.unsetColor];
        }
        if(outNumber == 1) {
          this.outColors = [this.unsetColor, this.setColor, this.unsetColor];
        }
        if(outNumber == 2) {
          this.outColors = [this.unsetColor, this.setColor, this.setColor];
        }
      },
      setBalls(ballNumber) {
        this.ballNumber = ballNumber;
        console.log('Changed number of balls:', ballNumber)
        if(ballNumber == 0) {
          this.ballColors = [this.set0Color, this.unsetColor, this.unsetColor, this.unsetColor];
        }
        if(ballNumber == 1) {
          this.ballColors = [this.unsetColor, this.setColor, this.unsetColor, this.unsetColor];
        }
        if(ballNumber == 2) {
          this.ballColors = [this.unsetColor, this.setColor, this.setColor, this.unsetColor];
        }
        if(ballNumber == 3) {
          this.ballColors = [this.unsetColor, this.setColor, this.setColor, this.setColor];
        }
      },
      setStrikes(strikeNumber) {
        this.strikeNumber = strikeNumber;
        console.log('Changed number of strikes:', strikeNumber)
        if(strikeNumber == 0) {
          this.strikeColors = [this.set0Color, this.unsetColor, this.unsetColor];
        }
        if(strikeNumber == 1) {
          this.strikeColors = [this.unsetColor, this.setColor, this.unsetColor];
        }
        if(strikeNumber == 2) {
          this.strikeColors = [this.unsetColor, this.setColor, this.setColor];
        }
      },
    },
    created() {
      // Fill inning and score selection lists
      this.scores.push(0);
      for (let i = 1; i <= 99; i++) {
        this.innings.push(`${i}∧`, `${i}∨`);
        this.scores.push(i);
      }

      // Set game state button colors
      this.baseColors = [this.unsetColor, this.unsetColor, this.unsetColor];
      this.outColors = [this.set0Color, this.unsetColor, this.unsetColor];
      this.ballColors = [this.set0Color, this.unsetColor, this.unsetColor, this.unsetColor];
      this.strikeColors = [this.set0Color, this.unsetColor, this.unsetColor];

      // Fill team selection lists
      const path = "http://localhost:5000/get_teams";
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
      gameState() {
        return {
          inning: this.inning, 
          outs: this.outNumber, 
          strikes: this.strikeNumber,
          balls: this.ballNumber, 
          home_score: this.home.score, 
          away_score: this.away.score
        };
      }
    },
    mounted() {

      // Sets current pitcher name/id and resets image
      this.emitter.on("ChangePitcher2", pitcher_obj => {

        this.curr_pitcher_id = pitcher_obj.id

      });
    },
  };
</script>
  