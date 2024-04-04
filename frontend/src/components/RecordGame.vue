<template>
      <v-card style="width: 100%; margin: 10px 10px;" 
        elevation="3"
      >
        <v-row>
          <!--Game state column-->
          <v-col cols="8">
            <v-container fluid>
                <!--Team selection and score-->
                <SelectTeams/>

                <!--Count and Inning Row-->
                <v-row>
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
                            @update:modelValue="handleInningChange"
                            variant="solo-filled"
                            density="compact" 
                            class="inning-v-select"
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
                        <v-col v-for="out in 3" :key="out" cols="2">
                          <v-chip 
                            @click="setOuts(out - 1)" 
                            :style="{backgroundColor: outColors[out - 1]}" 
                            size="x-small" class="mr-1"
                          >
                            {{ out - 1 }}
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
                        <v-col v-for="ball in 4" :key="ball" cols="2">
                          <v-chip 
                            @click="setBalls(ball - 1)" 
                            :style="{backgroundColor: ballColors[ball - 1]}"
                            size="x-small" class="mr-1"
                          >
                            {{ ball - 1 }}
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
                        <v-col v-for="strike in 3" :key="strike" cols="2">
                          <v-chip 
                            @click="setStrikes(strike - 1)" 
                            :style="{backgroundColor: strikeColors[strike - 1]}"
                            size="x-small" class="mr-1"
                          >
                            {{ strike - 1 }}
                          </v-chip>
                        </v-col>
                      </v-row>

                    </v-col>
                </v-row>
            </v-container>
          </v-col>
  
          <!--Input pitch column-->
          <v-col cols="4" class="d-flex flex-column justify-center text-center pr-5">
            <!--Input pitch dialog-->
            <v-row>
              <v-col>
                <InputPitch class="record-btn"/>
              </v-col>
            </v-row>

            <!--Start/stop game record button-->
            <v-row>
              <v-col>
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

          </v-col>
        </v-row>
      </v-card>
</template>

<script>
  import InputPitch from "@/components/InputPitch.vue";
  import SelectTeams from "@/components/SelectTeams.vue";

  export default {
    components: {
      InputPitch,
      SelectTeams,
    },
    data() {
      return {
        colors: {
          unset: '#EEEEEE',
          set: '#43A047',
          set0: 'gray',
        },
        recording: false,
        inning: "1∧",
        innings: [],
        onBase: [false, false, false],
        baseColors: [],
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
      handleGameButtonClick() {
        console.log('Game Button clicked!');
        if (this.recording) {
          this.recording = false;
        }
        else {
          this.recording = true;
        }
      },
      toggleBase(baseNumber) {
        console.log('Toggled base:', baseNumber);
        const i = baseNumber - 1;
        this.onBase[i] = !this.onBase[i];
        if(!this.onBase[i]){
          this.baseColors[i] = this.colors.unset;
        }
        else{
          this.baseColors[i] = this.colors.set;
        }
      },
      setOuts(outNumber) {
        this.outNumber = outNumber;
        console.log('Changed number of outs:', outNumber)
        if(outNumber == 0) {
          this.outColors = [this.colors.set0, this.colors.unset, this.colors.unset];
        }
        if(outNumber == 1) {
          this.outColors = [this.colors.unset, this.colors.set, this.colors.unset];
        }
        if(outNumber == 2) {
          this.outColors = [this.colors.unset, this.colors.set, this.colors.set];
        }
      },
      setBalls(ballNumber) {
        this.ballNumber = ballNumber;
        console.log('Changed number of balls:', ballNumber)
        if(ballNumber == 0) {
          this.ballColors = [this.colors.set0, this.colors.unset, this.colors.unset, this.colors.unset];
        }
        if(ballNumber == 1) {
          this.ballColors = [this.colors.unset, this.colors.set, this.colors.unset, this.colors.unset];
        }
        if(ballNumber == 2) {
          this.ballColors = [this.colors.unset, this.colors.set, this.colors.set, this.colors.unset];
        }
        if(ballNumber == 3) {
          this.ballColors = [this.colors.unset, this.colors.set, this.colors.set, this.colors.set];
        }
      },
      setStrikes(strikeNumber) {
        this.strikeNumber = strikeNumber;
        console.log('Changed number of strikes:', strikeNumber)
        if(strikeNumber == 0) {
          this.strikeColors = [this.colors.set0, this.colors.unset, this.colors.unset];
        }
        if(strikeNumber == 1) {
          this.strikeColors = [this.colors.unset, this.colors.set, this.colors.unset];
        }
        if(strikeNumber == 2) {
          this.strikeColors = [this.colors.unset, this.colors.set, this.colors.set];
        }
      },
    },
    created() {
      // Fill inning selection list
      for (let i = 1; i <= 99; i++) {
        this.innings.push(`${i}∧`, `${i}∨`);
      }
      // Set game state button colors
      this.baseColors = [this.colors.unset, this.colors.unset, this.colors.unset];
      this.outColors = [this.colors.set0, this.colors.unset, this.colors.unset];
      this.ballColors = [this.colors.set0, this.colors.unset, this.colors.unset, this.colors.unset];
      this.strikeColors = [this.colors.set0, this.colors.unset, this.colors.unset];
    },
    computed: {
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
    margin-top: 5px;
    margin-bottom: 5px;
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