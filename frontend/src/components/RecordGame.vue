<template>
    <v-container fluid>
      <v-card>
        <v-row>
          <!--Game state column-->
          <v-col cols="9">
            <v-container fluid>
                <v-row class="text-center my-label">
                    <v-col cols="4">
                      <v-select
                        :items="homeTeams"
                        density="compact"
                        label="Home Team"
                      ></v-select>
                    </v-col>
                    <!--Score input-->
                    <v-col cols="4">
                      <v-container fluid>
                        <v-row>
                          <!--Home Score and "-"-->
                          <v-col>
                                <v-text-field
                                  v-model="homeScore"
                                  :rules="scoreRules"
                                  label="Score"
                                  density="compact"
                                  class="home-score-v-text-field"
                                  hide-details
                                ></v-text-field>
                          </v-col>
                          <v-col class="mt--10 text-center">
                            <p>-</p>
                          </v-col>
                          <!--Away Score-->
                          <v-col>
                              <v-text-field
                                v-model="awayScore"
                                :rules="scoreRules"
                                label="Score"
                                density="compact"
                                class="away-score-v-text-field"
                                hide-details
                              ></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-col>
                    <v-col cols="4">
                        <v-select
                          :items="awayTeams"
                          density="compact"
                          label="Away Team"
                        ></v-select>
                    </v-col>
                </v-row>


                <!--Score and Inning Row-->
                <v-row>
                    <!--Runners on base-->
                    <v-col></v-col>
                    <!--Innings and count-->
                    <v-col>
                      <v-row>
                        <v-select
                          :items="innings"
                          density="compact"
                          label="In."
                          class="my-v-select"
                        ></v-select>
                      </v-row>
                      <v-row>
                        <v-select
                          :items="innings"
                          density="compact"
                          label="Outs"
                          class="my-v-select"
                        ></v-select>
                      </v-row>
                    </v-col>
                </v-row>
            </v-container>

            <v-row>
                <v-btn 
                    @click="handleGameButtonClick"
                    class="mx-auto ma-5"
                >
                    Start Game
                </v-btn>
            </v-row>
          </v-col>
  
          <!--Input pitch column-->
          <v-col cols="3">
            <v-row>
              <v-container fluid>
                  <!--Input pitch dialog-->
                  <v-dialog width="500">
                      <template v-slot:activator="{ props }">
                          <v-img 
                              src="@/assets/strikezone.jpg"
                              v-bind="props"
                              class="mr-5 ml--20"
                              max-height="250"
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
              </v-container>
            </v-row>
            <!--Predict button-->
            <v-row>
              <v-col>
                <v-btn 
                    class="mx-auto mb-7"
                    @click="handlePredictButtonClick"
                >
                    Predict
                </v-btn>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  </template>
  
<style>
.my-v-text-field.v-text-field--solo .v-input__control {
    min-height: 10px;
}
.my-v-select .v-select__selection {
  font-size: 6px; 
}
.label {
  font-size: 12px;
}
.my-v-select {
  margin-top: -20px;
}
.home-score-v-text-field {
  margin-left: -25px; 
  margin-right: -20px;
  margin-top: -16px;
  min-width: 0;
  padding: 0;
}
.away-score-v-text-field { 
  margin-left: -20px; 
  margin-right: -25px;
  margin-top: -16px; 
}
.my-label label {
  font-size: 10px;
  width: 100%;
}
</style>

  <script>
  export default {
    data() {
      return {
        selectedItem1: null,
        selectedItem2: null,
        homeTeams: ['Team1', 'Team2', 'Team3'],
        awayTeams: ['Team1', 'Team2', 'Team3'],
        innings: ['1∧', '1∨','2∧', '2∨', '3∧', '3∨'],
        topBottom: ['∧', '∨']
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
    },
  };
  </script>
  