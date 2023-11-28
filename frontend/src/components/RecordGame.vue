<template>
    <v-container fluid>
      <v-card>
        <v-row>
          <!--Game state column-->
          <v-col cols="9">
            <v-container fluid>
                <v-row class="text-center">
                    <!--Input home team-->
                    <v-col cols="6">
                      <v-select
                        :items="homeTeams"
                        density="compact"
                        label="Home Team"
                        class="my-label"
                        variant="filled"
                      ></v-select>
                    </v-col>
                    <!--Input away team-->
                    <v-col cols="6">
                        <v-select
                          :items="awayTeams"
                          density="compact"
                          label="Away Team"
                          class="my-label"
                          variant="filled"
                        ></v-select>
                    </v-col>
                </v-row>
                
                <!--Score input-->
                <v-row>
                          <!--Home Score and "-"-->
                          <v-col align="right" cols="5">
                                <v-text-field
                                  v-model="homeScore"
                                  :rules="scoreRules"
                                  label="Score"
                                  density="compact"
                                  class="score-v-text-field my-label"
                                  hide-details
                                  variant="solo-filled"
                                ></v-text-field>
                          </v-col>
                          <v-col 
                            cols="2"
                            class="score-spacer text-center"
                          >
                            <p>-</p>
                          </v-col>
                          <!--Away Score-->
                          <v-col align="left" cols="5">
                              <v-text-field
                                v-model="awayScore"
                                :rules="scoreRules"
                                label="Score"
                                density="compact"
                                class="score-v-text-field my-label"
                                variant="solo-filled"
                                hide-details
                              ></v-text-field>
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
                              class="square-chip"
                              size="small"
                            >2</v-chip>
                          </v-col>
                        </v-row>

                        <!--First and third base-->
                        <v-row class="mt-0">
                          <v-spacer></v-spacer>
                          <v-col class="text-center">
                            <v-chip
                              @click="toggleBase(3)"
                              class="square-chip"
                              size="small"
                            >3</v-chip>
                          </v-col>
                          <v-col class="text-center">
                            <v-chip
                              @click="toggleBase(1)"
                              class="square-chip"
                              size="small"
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
                          <v-chip size="x-small" class="mr-1">0</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip size="x-small" class="mr-1">1</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip size="x-small" class="mr-1">2</v-chip>
                        </v-col>
                      </v-row>
                      
                      <!--Balls-->
                      <v-row no-gutters class="no-wrap mt-2">
                        <v-col align="right" cols="4" class="my-font">
                          <p class="out-ball-strike-text">Balls</p>
                        </v-col>
                        <v-col cols="2">
                          <v-chip size="x-small" class="mr-1">0</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip size="x-small" class="mr-1">1</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip size="x-small" class="mr-1">2</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip size="x-small" class="mr-1">3</v-chip>
                        </v-col>
                      </v-row>

                      <!--Strikes-->
                      <v-row no-gutters class="no-wrap mt-2">
                        <v-col align="right" cols="4" class="my-font">
                          <p class="out-ball-strike-text">Strikes</p>
                        </v-col>
                        <v-col cols="2">
                          <v-chip size="x-small" class="mr-1">0</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip size="x-small" class="mr-1">1</v-chip>
                        </v-col>
                        <v-col cols="2">
                          <v-chip size="x-small" class="mr-1">2</v-chip>
                        </v-col>
                      </v-row>

                    </v-col>
                </v-row>
            </v-container>
          </v-col>
  
          <!--Input pitch column-->
        <v-col cols="3" class="d-flex flex-column justify-center">
              <!--Input pitch dialog-->
                <div>
                    <v-dialog width="500">
                        <template v-slot:activator="{ props }">
                            <v-img
                                src="@/assets/strikezone.png"
                                v-bind="props"
                                class="input-pitch-v-dialog"
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
                class="predict-btn"
                @click="handlePredictButtonClick"
              >Predict</v-btn>   

            <!--Start/stop game record button-->
                <v-btn 
                    prepend-icon="mdi-record-circle"
                    @click="handleGameButtonClick"
                    class="start-stop-game-btn"
                >
                    Start<br>Game
                </v-btn>

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
    margin-top: 2px;
    margin-bottom: 5px;
  }
  .start-stop-game-btn {
    width: 75%;
    min-width: 80px;
    margin-top: 5px;
    margin-bottom: 5px;
  }
  .predict-btn {
    min-width: 80px;
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
  export default {
    data() {
      return {
        homeScore: '',
        awayScore: '',
        homeTeams: ['Team1', 'Team2', 'Team3'],
        awayTeams: ['Team1', 'Team2', 'Team3'],
        innings: ['1∧', '1∨','2∧', '2∨', '3∧', '3∨', '4∧', '4∨','5∧', '5∨', '6∧', '6∨', '7∧', '7∨','8∧', '8∨', '9∧', '9∨', '10∧', '10∨','11∧', '11∨', '12∧', '12∨', '13∧', '13∨','14∧', '14∨', '15∧', '15∨', '16∧', '16∨','17∧', '17∨', '18∧', '18∨', '19∧', '19∨','20∧', '20∨', '21∧', '21∨', '22∧', '22∨','23∧', '23∨', '24∧', '24∨', '25∧', '25∨','26∧', '26∨', '27∧', '27∨', '28∧', '28∨','29∧', '29∨', '30∧', '30∨', '31∧', '31∨','32∧', '32∨', '33∧', '33∨', '34∧', '34∨','35∧', '35∨', '36∧', '36∨'],
        outs: ['0', '1', '2', '3'],
        balls: ['0', '1', '2', '3', '4'],
        strikes: ['0', '1', '2', '3']
      };
    },
    methods: {
      handleGameButtonClick() {
        console.log('Game Button clicked!');
        // Start or stop game recording
      },
      handlePredictButtonClick() {
        console.log('Predict Button clicked!');
        // Generate next prediction
      },
      toggleBase(baseNumber) {
        console.log('Toggled base:', baseNumber);
      },
    },
  };
</script>
  