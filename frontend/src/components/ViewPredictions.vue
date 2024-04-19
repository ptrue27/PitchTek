<template>
    <v-card style="width: 100%; margin: 10px 10px; border: 2px solid #43A047;" 
      elevation="3"
    >
      <!-- Displaying Paginated Data -->
      <v-list>
        <v-list-item-group>
          <v-list-item v-for="(item, index) in currentData" :key="item.id">
            <!-- Content for each row -->
            <v-list-item-content>
                <v-row>
                  <!--Prediction image-->
                    <v-col cols="6">
                        <v-img :src=imageURLs[index] style="margin-top: 5px; margin-bottom: 5px; height: 392px;"
                        ></v-img>
                    </v-col>

                    <!--Predicted values-->
                    <v-col cols="6">
                        <v-row style="margin-top: 75px;">
                            <v-col class="predict-col">Confidence:</v-col>
                            <v-col class="predict-data-col">{{ predictions[index].confidence }}%</v-col>
                        </v-row>
                        <v-row class="predict-row">
                          <v-col class="predict-col">Pitch type:</v-col>
                          <v-col class="predict-data-col">{{ predictions[index].type }}</v-col>
                        </v-row>
                        <v-row class="predict-row">
                          <v-col class="predict-col">Speed:</v-col>
                          <v-col class="predict-data-col">{{ predictions[index].speed }} mph</v-col>
                        </v-row>
                        <v-row class="predict-row">
                          <v-col class="predict-col">Location:</v-col>
                          <v-col class="predict-data-col">Zone {{ predictions[index].location }}</v-col>
                        </v-row>
                    </v-col>
                </v-row>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>

      <!-- Pagination Controls -->
      <v-card-actions class="text-center border-top pt-3">
        <v-row>
          <v-col>
            <v-btn
                @click="prevPage"
                :disabled="currentPage === 0"
            >
                <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
            <span>{{ currentPage + 1 }}</span>
            <v-btn @click="nextPage" :disabled="currentPage === pages.length - 1">
                <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-actions>

    </v-card>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'my-component',
  data() {
    return {
      pitchDict: {
        FA:   "Fastball",
        FF:   "Fastball",
        FT:   "Fastball",
        FC:   "Fastball (Cutter)",
        FS:   "Splitter",
        CH:   "Changeup",
        CU:   "Curveball",
        EP:   "Eephus",
        FO:   "Forkball",
        KN:   "Knuckleball",
        KC:   "Knuckle-curve",
        SC:   "Screwball",
        SI:   "Sinker",
        SL:   "Slider",
        SV:   "Slurve",
        ST:   "Sweeper",
        PO:   "Pitch Out",
        NA:   ""
      },
      itemsPerPage: 1,
      currentPage: 0,
      pages: [],
    };
  },
  created() {
    this.pages = Array.from({ length: Math.ceil(this.predictions.length / this.itemsPerPage) }, (_, index) => {
      const startIndex = index * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.predictions.slice(startIndex, endIndex);
    });
  },
  computed: {
    ...mapState({
        pitcherId: state => state.current.pitcher.id,
        predictions: state => state.predictions,
    }),
    currentData() {
      return this.pages[this.currentPage] || [];
    },
    imageURLs(){
      return [
        require("@/assets/heat_maps/" + this.predictions[0].img),
        require("@/assets/heat_maps/" + this.predictions[1].img),
        require("@/assets/heat_maps/" + this.predictions[2].img),
      ]
    },
  },
  methods: {
    prevPage() {
      this.currentPage = Math.max(this.currentPage - 1, 0);
    },
    nextPage() {
      console.log(this.predictions.length + "::" + this.predictions[0].type + this.predictions[1].type);
      this.currentPage = Math.min(this.currentPage + 1, this.predictions.length - 1);
    },

  },
  /*mounted() {
    this.emitter.on("ChangePitch", my_var => {
      console.log('ChangePitch() called, with pitch:', my_var[0]);
      this.data[0].type = my_var[0]
      this.data[0].speed = my_var[1]

      this.predictionImg = this.curr_pitcher_id + "_" + my_var[0] + "_heat_map.jpg"
      console.log("this image: " + this.imageURL)
    });

    // Sets current pitcher name/id and resets image
    this.emitter.on("ChangePitcher", pitcher_obj => {

      // If heat maps for pitcher does not exist, make images
      // this.checkFileExists("@/assets/heat_maps/default_heat_map.jpg")

      this.curr_pitcher_id = pitcher_obj.id

      // Set values to default
      this.image_path = "default_heat_map.jpg"
      this.data[0].type = ""
      this.data[0].speed = ""

    });
  },*/
};
</script>

<style>
  .border-top {
    border-top: 1px solid gray;
    background-color: #F2F2F2;
  }
  .prediction-number {
      white-space: nowrap;
      text-align: center;
      font-size: 10px;
      padding-left: 2px;
  }
  .predict-col {
    margin-left:50px;
    font-weight: bold;
    font-size: 18px;
  }
  .predict-data-row {
    margin-left: 50px;
    font-size: 18px;
  }
  .predict-row {
    padding-top: 20px;
  }
</style>