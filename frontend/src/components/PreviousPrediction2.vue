<template>
  <v-container fluid class="custom-style">
    <v-card>
      <v-row>
        <!--Game state column-->
        <v-col cols="8">
          <v-container fluid class="custom-style-2">
            <v-row class="text-center" style="margin-bottom: -40px;">
              <!--Input home team-->
              <v-col cols="6">
                <v-text-field
                  :value=HomeTeamName
                  density="compact"
                  variant="solo-filled"
                  readonly
                ></v-text-field>
              </v-col>
              <!--Input away team-->
              <v-col cols="6">
                <v-text-field
                  :value="AwayTeamName"
                  variant="filled"
                  density="compact"
                  class="my-label team-name"
                  readonly
                ></v-text-field>
              </v-col>
            </v-row>

            <!--HomeScore input-->
            <v-row class="HomeScore-row">
              <!--Home HomeScore and "-"-->
              <v-col cols="3" style="margin-top: 10px;" align="right">
                <p style="margin-right: 10px;">Home</p>
              </v-col>
              <v-col cols="2">
                <v-text-field
                  :value="HomeScore"
                  variant="filled"
                  density="compact"
                  class="my-label team-name"
                  readonly
                ></v-text-field>
              </v-col>
              <v-col
                cols="2"
                style="margin-top: -2px; margin-left: -10px; margin-right: -10px;"
                class="HomeScore-spacer text-center"
              >
                <p>-</p>
              </v-col>
              <!--Away Score-->
              <v-col cols="2">
                <v-text-field
                  :value="AwayScore"
                  density="compact"
                  variant="solo-filled"
                  readonly
                ></v-text-field>
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
                        :style="{backgroundColor: baseColors[1]}"
                        class="square-chip" size="small"
                        disabled
                      >2</v-chip>
                    </v-col>
                  </v-row>

                  <!--First and third base-->
                  <v-row class="mt-0">
                    <v-spacer></v-spacer>
                    <v-col class="text-center">
                      <v-chip
                        :style="{backgroundColor: baseColors[2]}"
                        class="square-chip" size="small"
                        disabled
                      >3</v-chip>
                    </v-col>
                    <v-col class="text-center">
                      <v-chip
                        :style="{backgroundColor: baseColors[0]}"
                        class="square-chip" size="small"
                        disabled
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
                      ></v-img>
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
                    <v-text-field
                      :value=Inning
                      variant="solo-filled"
                      density="compact"
                      class="inning-v-select"
                      readonly
                    ></v-text-field>
                  </v-col>
                </v-row>


              </v-col>
            </v-row>
          </v-container>
        </v-col>

        <!--Pitch input column-->
        <v-col cols="4">
          <v-row>
            <v-col class="text-center">
              <v-img
                :src=ImageURL
                class="mx-auto"
                height="300px"
              ></v-img>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>



<script>
export default {
    props: {
      HomeTeamName: String,
      HomeScore: Number,
      AwayTeamName: String,
      AwayScore: Number,
      Inning: String,
      pitchType: String,
      pitcherId: String,
      baseColors: [String, String, String]
  },
  data: () => ({
    outs: "0",
    balls: "0",
    strikes: "0",
    countColors: {
      outs: '#FFF',
      balls: '#FFF',
      strikes: '#FFF'
    }
  }),
  computed: {
    ImageURL(){
      return require("@/assets/heat_maps/" + this.pitcherId + "_" + this.pitchType + "_heat_map.jpg")
    },
  },
};
</script>

<style scoped>
.my-font {
  font-size: 12px;
}
.team-name {
  font-size: 18px;
}
.square-chip {
    width: 25px;
    height: 25px;
    //background-color: lightblue !important; /* Temporary to test visibility */
    border: black;
    opacity: 1 !important; /* Ensure it's fully opaque */
}
.inning-text, .out-ball-strike-text {
  margin: 0;
  padding: 0;
}
.inning-v-select, .out-ball-strike-chip {
  width: 50px;
  height: 25px;
}
.custom-style {
  background-color: #a9c5d2; /* Light blue background */
  border: 20px solid #5d5daf; /* Blue border */
  padding: 0px; /* Adds space inside the border */
  box-sizing: border-box; /* Includes padding and border in the element's size */
}
.custom-style-2 {
  background-color: #ffffff; /* Light blue background */
}
</style>
