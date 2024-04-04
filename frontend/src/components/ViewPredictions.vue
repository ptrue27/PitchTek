<template>
    <v-card style="width: 100%; margin: 10px 10px;" 
      elevation="3"
    >
      <!-- Displaying Paginated Data -->
      <v-list>
        <v-list-item-group>
          <v-list-item v-for="item in currentData" :key="item.id">
            <!-- Content for each row -->
            <v-list-item-content>
                <v-row>
                    <v-col cols="5">
                        <v-img
                            :src=imageURL
                        ></v-img>
                        <v-card-title>{{curr_pitcher_name}}</v-card-title>
                    </v-col>
                    <!--Innings and count-->
                    <v-col cols="7">
                        <!--Title-->
                        <v-row>
                            <v-col class="my-title">Confidence: {{item.confidence}}%</v-col>
                        </v-row>
                        <!--Pitch info-->
                        <v-row>
                            <v-col>Pitch type:</v-col>
                            <v-col>{{item.type}}</v-col>
                        </v-row>
                        <v-row>
                            <v-col>Speed:</v-col>
                            <v-col>{{item.speed}} mph</v-col>
                        </v-row>
                        <v-row>
                            <v-col>Location:</v-col>
                            <v-col>({{item.locationX}}, {{item.locationY}})</v-col>
                        </v-row>
                    </v-col>
                </v-row>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>

      <!-- Pagination Controls -->
      <v-card-actions class="text-center">
        <v-container class="pb-0">
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
        </v-container>
      </v-card-actions>

    </v-card>
</template>

<style>
.my-title {
    white-space: nowrap;
    text-align: center;
}
.prediction-number {
    white-space: nowrap;
    text-align: center;
    font-size: 10px;
    padding-left: 2px;
}
</style>

<script>
export default {
  name: 'my-component',
  data() {
    return {
      image_path: "default_heat_map.jpg",
      curr_pitcher_name: "",
      curr_pitcher_id: "NA",
      currentimage : 0,
      data: [
        {id: 1, confidence: 'NA', type: 'NA', speed: 'NA', locationX: 'NA', locationY: 'NA'},
        {id: 2, confidence: 'NA', type: 'NA', speed: 'NA', locationX: 'NA', locationY: 'NA'},
        {id: 3, confidence: '7.04', type: 'Slider', speed: 82.27, locationX: 78, locationY: 38},
      ],
      itemsPerPage: 1,
      currentPage: 0,
      pages: [],
    };
  },
  created() {
    this.pages = Array.from({ length: Math.ceil(this.data.length / this.itemsPerPage) }, (_, index) => {
      const startIndex = index * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.data.slice(startIndex, endIndex);
    });
  },
  computed: {
    currentData() {
      return this.pages[this.currentPage] || [];
    },
    predictionImgSrc() {
      //return this.$store.state.predictionImgSrc
      //console.log("predictionImgSrc called")
      return require(this.imageURL)
    },
    imageURL(){
      return require("@/assets/heat_maps/" + this.image_path)
    },
  },
  methods: {
    prevPage() {
      this.currentPage = Math.max(this.currentPage - 1, 0);
    },
    nextPage() {
      this.currentPage = Math.min(this.currentPage + 1, this.data.length - 1);
    },
    /*checkFileExists(my_URL) {
      fetch(my_URL)
        .then(response => {
          if (response.ok) {
            console.log("this.fileExists = true; URL: ", my_URL)
          } else {
            console.log("this.fileExists = false; URL: ", my_URL)
          }
        })
        .catch(error => {
          console.error('Error checking file existence:', error);
          console.log("this.fileExists = false; URL: ", my_URL)
        });
    }*/
  },
    mounted() {
      this.emitter.on("ChangePitch", my_var => {
        console.log('ChangePitch() called, with pitch:', my_var[0]);
        this.data[0].type = my_var[0]
        this.data[0].speed = my_var[1]

        this.image_path = this.curr_pitcher_id + "_" + my_var[0] + "_heat_map.jpg"
        console.log("this image: " + this.imageURL)
      });

      // Sets current pitcher name/id and resets image
      this.emitter.on("ChangePitcher", pitcher_obj => {

        // If heat maps for pitcher does not exist, make images
        // this.checkFileExists("@/assets/heat_maps/default_heat_map.jpg")

        this.curr_pitcher_name = pitcher_obj.name
        this.curr_pitcher_id = pitcher_obj.id

        // Set values to default
        this.image_path = "default_heat_map.jpg"
        this.data[0].type = ""
        this.data[0].speed = ""

      });
    },
};
</script>