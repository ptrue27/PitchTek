<template>
    <v-container fluid>
      <v-card>
        <v-row>
          <!-- Left Column -->
          <v-col cols="8">
            <v-container fluid>
                <v-row class="text-center">
                    <v-col>
                        <p>Team 1</p>
                    </v-col>
                    <v-col>
                        <p>3 - 6</p>
                    </v-col>
                    <v-col>
                        <p>Team 2</p>
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
  
          <!-- Right Column -->
          <v-col cols="4">
            <v-row>
                <v-dialog width="500">
                    <template v-slot:activator="{ props }">
                        <v-img 
                            src="@/assets/strikezone.jpg"
                            v-bind="props"
                            class="ma-5"
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
            </v-row>
            <v-row>
                <v-btn 
                    class="mx-auto ma-5"
                    @click="handlePredictButtonClick"
                >
                    Predict
                </v-btn>
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  </template>
  
  <script>
  export default {
    data() {
      return {
        selectedItem1: null,
        selectedItem2: null,
        dropdownItems: ['Option 1', 'Option 2', 'Option 3'],
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
  