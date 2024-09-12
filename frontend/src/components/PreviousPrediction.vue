<template>
  <v-card style="width: 100%; margin: 10px;" 
    elevation="3" class="card-border"
  >
    <v-card-text>
      <v-row style="margin-top: -16px; margin-bottom: -16px; margin-left: -16px;">
        <!-- First Column with Text -->
        <!--Game state column-->
        <v-col cols="4" style="border-right: 2px solid #43A047;">
          <div>
            <!--Team selection and score-->
            <v-row style="border-bottom: 2px solid #43A047;">
              <v-col>
                <!--Team selection-->
                <v-row class="text-center" style="margin-bottom: -40px; margin-left: 3px; margin-top: 3px; margin-right: 3px;">
                    <!--Input home team-->
                    <v-col cols="5" style="font-size: 16px">
                        {{storeSnapshot.home_name}}
                    </v-col>
                    <v-col cols="2" class="text-center" style="padding-top: 15px;">
                        vs.
                      </v-col>
                    <!--Input away team-->
                    <v-col cols="5" style="font-size: 16px;">
                        {{storeSnapshot.away_name}}
                    </v-col>
                </v-row>
                          
                <!--Score input-->
                <v-row style="margin-bottom: 5px; margin-top: 40px">
                    <!--Home Score-->
                    <v-col cols="3" style="margin-top: 15px;" align="right">
                        <p class="home-away" style="margin-right: 30px;">
                            Home
                        </p>
                    </v-col>
                    <v-col cols="2">
                  <select disabled class="vuetify-like-dropdown">
                    <option selected>{{storeSnapshot.home_score}}</option>
                  </select>
                    </v-col>

                    <v-col cols="2" class="score-spacer text-center" style="margin-top: 10px;">
                        <p>-</p>
                    </v-col>
                    
                    <!--Away Score-->
                    <v-col cols="2">
                  <select disabled class="vuetify-like-dropdown">
                    <option selected>{{storeSnapshot.away_score}}</option>
                  </select>
                    </v-col>
                    <v-col cols="3" style="margin-top: 15px;" align="left">
                        <p class="home-away" style="margin-left: 30px;">
                            Away
                        </p>
                    </v-col>
                </v-row>
              </v-col>
            </v-row>

            <!--Runners on Base/Count and Inning Row-->
            <v-row style="margin-top: 35px; margin-bottom: 3px; padding-right: 25px;">
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
                          :style="{backgroundColor: getBaseColor(storeSnapshot.base_second)}"
                          :class="{'square-chip': true, 'unclickable': true}"
                          size="small"
                      >2
                      </v-chip>
                    </v-col>
                  </v-row>

                  <!--First and third base-->
                  <v-row class="mt-0">
                    <v-spacer></v-spacer>
                    <v-col class="text-center">
                      <v-chip
                          :style="{backgroundColor: getBaseColor(storeSnapshot.base_third)}"
                          :class="{'square-chip': true, 'unclickable': true}"
                          size="small"
                      >3
                      </v-chip>
                    </v-col>
                    <v-col class="text-center">
                      <v-chip
                          :style="{backgroundColor: getBaseColor(storeSnapshot.base_first)}"
                          :class="{'square-chip': true, 'unclickable': true}"
                          size="small"
                      >1
                      </v-chip>
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
                    <select disabled class="vuetify-like-dropdown">
                      <option selected>{{storeSnapshot.inning}}</option>
                    </select>
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
                        :style="{backgroundColor: getColor(
                              storeSnapshot.outs, index)}"
                        :class="{'mr-1': true, 'unclickable': true}"
                        size="x-small"
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
                        :style="{backgroundColor: getColor(
                              storeSnapshot.balls, index)}"
                        :class="{'mr-1': true, 'unclickable': true}"
                        size="x-small"
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
                        :style="{backgroundColor: getColor(
                              storeSnapshot.strikes, index)}"
                        :class="{'mr-1': true, 'unclickable': true}"
                        size="x-small"
                    >
                      {{ index }}
                    </v-chip>
                  </v-col>
                </v-row>

              </v-col>
            </v-row>
          </div>
        </v-col>

        <!-- Second Column -->
        <v-col cols="2">
          <v-row>
            <v-col>
                <v-img v-if="storeSnapshot.pitcher_img"
                  :src="storeSnapshot.pitcher_img"
                  style="height: 125px;"
                  class="align-self-center"
                ></v-img>
                <v-img v-else
                  src="@/assets/silhouette.png"
                  style="height: 125px;"
                  class="align-self-center"
                ></v-img>
                <div><b>Pitcher</b></div>
                <div>{{storeSnapshot.pitcher_name}}</div>
            </v-col>
          </v-row>
          <v-row style="margin-top: 0px;">
            <v-col>
              <v-img v-if="storeSnapshot.batter_img"
                :src="storeSnapshot.batter_img"
                style="height: 125px;"
                class="align-self-center"
              ></v-img>
              <v-img v-else
                src="@/assets/silhouette.png"
                style="height: 125px;"
                class="align-self-center"
              ></v-img>
              <div><b>Batter</b></div>
              <div>{{storeSnapshot.batter_name}}</div>
            </v-col>
          </v-row>
        </v-col>

        <!-- Third Column with Image -->
        <v-col cols="3" class="previous-prediction-image-container">
          <img :src="imageURL" alt="Pitch prediction heatmap"/>
        </v-col>

        <!-- Fourth Column with Text -->
        <v-col cols="3" style="border-right: #43A047 solid 6px;">
          <v-row style="margin-top: 25px;">
            <v-col class="predict-col">
              Confidence:
            </v-col>
            <v-col class="predict-data-col">{{ storeSnapshot.prediction_confidence }}%</v-col>
          </v-row>
          <v-row class="predict-row">
            <v-col class="predict-col">Pitch type:</v-col>
            <v-col class="predict-data-col">{{ storeSnapshot.prediction_type }}</v-col>
          </v-row>
          <v-row class="predict-row">
            <v-col class="predict-col">Speed:</v-col>
            <v-col class="predict-data-col">{{ storeSnapshot.prediction_speed }} mph</v-col>
          </v-row>
          <v-row class="predict-row">
            <v-col class="predict-col">Location:</v-col>
            <v-col class="predict-data-col">Zone {{ storeSnapshot.prediction_location}}</v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>


<script>
export default {
  props: {
    storeSnapshot: {
      type: Object,
      required: true
    }
  },
  computed: {
    imageURL() {

      try {
        return require("@/assets/heat_maps_v2/" + this.prediction.img)

      } catch (error) {
        return require("@/assets/heat_maps_v2/default_heat_map.jpg")
      }

    },
  },
  methods: {
    getColor(state, index) {
      if (state == index) {
        if (index == 0) {
          return 'gray';
        } else {
          return '#43A047';
        }
      } else {
        return '#EEEEEE';
      }
    },
    getBaseColor(baseValue) {
      if (baseValue) {
        return '#43A047';
      } else {
        return '#EEEEEE';
      }
    },
  }
};
</script>

<style>
.previous-prediction-image-container img {
  height: 350px;
  width: auto;
}
.previous-prediction-image-container {
  flex: 1;
}
.unclickable {
  pointer-events: none; /* Clicks won't register, but all styles remain */
}
.vuetify-like-dropdown {
  font-family: 'Roboto', sans-serif; /* Vuetify default font */
  border: 1px solid rgb(0, 0, 0); /* Mimic Vuetify's border */
  border-radius: 4px; /* Rounded corners like Vuetify inputs */
  padding: 10px 26px 10px 12px; /* Padding for text and arrow spacing */
  font-size: 16px; /* Standard font size */
  background-color: white; /* Background color */
  background-repeat: no-repeat; /* No-repeat for the background image */
  background-position: right 8px center; /* Position for the dropdown arrow */
  background-size: 24px; /* Size of the dropdown arrow */
  -webkit-appearance: none; /* Remove default styling */
  -moz-appearance: none; /* Remove default styling for Firefox */
  appearance: none; /* Standard way to remove default styling */
  color: black;
}
</style>
