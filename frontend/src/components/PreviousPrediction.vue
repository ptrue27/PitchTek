<template>
  <v-card style="width: 100%; margin: 10px; border: 2px solid #43A047;" elevation="3">
    <v-card-text>
      <v-row>
        <!-- First Column with Text -->
        <!--Game state column-->
        <v-col cols="4" style="border-right: 2px solid #43A047;">
          <div>
            <!--Team selection and score-->
            <v-row style="border-bottom: 2px solid #43A047;">
              <v-col>
                <SelectTeams :storeSnapshot="storeSnapshot" />
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
                          @click="this.$store.commit('toggleBase', 2)"
                          :style="{backgroundColor: getBaseColor(2)}"
                          :class="{'square-chip': true, 'unclickable': true}"
                          size="small"
                      >3
                      </v-chip>
                    </v-col>
                    <v-col class="text-center">
                      <v-chip
                          @click="this.$store.commit('toggleBase', 0)"
                          :style="{backgroundColor: getBaseColor(0)}"
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
                        @click="this.$store.commit('setOuts', index)"
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
                        @click="this.$store.commit('setBalls', index)"
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
        <v-col cols="12" md="3">
          <v-row align="center" justify="center">
            <v-col cols="5" class="text-center">
              <v-img v-if="storeSnapshot.pitcher_img"
                :src="storeSnapshot.pitcher_img"
                style="border: 1px solid black;"
                class="align-self-center"
              ></v-img>
              <div><b>Pitcher</b></div>
              <div>{{storeSnapshot.pitcher_name}}</div>
            </v-col>
            <v-col cols="2" class="text-center">vs</v-col>
            <v-col cols="5" class="text-center">
              <v-img v-if="storeSnapshot.batter_img"
                :src="storeSnapshot.batter_img"
                style="border: 1px solid black;"
                class="align-self-center"
              ></v-img>
              <div><b>Batter</b></div>
              <div>{{storeSnapshot.batter_name}}</div>
            </v-col>
          </v-row>
        </v-col>



        <!-- Third Column with Image -->
        <v-col cols="12" md="3" class="image-container">
          <img :src="imageURL" alt="Image"/>
        </v-col>

        <!-- Fourth Column with Text -->
        <v-col cols="2">
          <v-row style="margin-top: 25px;">
            <v-col class="predict-col">Confidence:</v-col>
            <v-col class="predict-data-col">{{ storeSnapshot.predictions[0].confidence }}%</v-col>
          </v-row>
          <v-row class="predict-row">
            <v-col class="predict-col">Pitch type:</v-col>
            <v-col class="predict-data-col">{{ storeSnapshot.predictions[0].type }}</v-col>
          </v-row>
          <v-row class="predict-row">
            <v-col class="predict-col">Speed:</v-col>
            <v-col class="predict-data-col">{{ storeSnapshot.predictions[0].speed }} mph</v-col>
          </v-row>
          <v-row class="predict-row">
            <v-col class="predict-col">Location:</v-col>
            <v-col class="predict-data-col">Zone {{ storeSnapshot.current.pitcher.name}}</v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>


<script>

import SelectTeams from "@/components/SelectTeamsUnclickable.vue";

export default {
  components: {
    SelectTeams
  },
  props: {
    storeSnapshot: {
      type: Object,
      required: true
    }
  },
  computed: {
    imageURL() {
      return require("@/assets/heat_maps_v2/" + this.storeSnapshot.predictions[0].img )
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
    getBaseColor(index) {
      if (this.storeSnapshot.bases[index]) {
        return '#43A047';
      } else {
        return '#EEEEEE';
      }
    },
  }
};
</script>

<style>
.image-container img {
  height: 300px;
  width: auto;
}
.image-container {
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
