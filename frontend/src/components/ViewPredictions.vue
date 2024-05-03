<template>
    <v-card style="width: 100%; margin: 10px 10px; " 
      elevation="3" class="card-border"
    >
      <!--Title-->
      <v-row class="border-bottom" style="margin-top: 0px; font-weight: bold">
          <v-col class="text-center">
              <div>Predicted Pitch</div>
          </v-col>
      </v-row>
  
      <v-row>
        <!--Prediction image-->
          <v-col cols="6">
              <v-img :src=imageURL style="margin-top: -3px; margin-bottom: 7px; height: 392px;"
              ></v-img>
          </v-col>

          <!--Predicted values-->
          <v-col cols="6">
              <v-row style="margin-top:60px;">
                  <v-col class="predict-col">Confidence:</v-col>
                  <v-col class="predict-data-col">{{ prediction.confidence }}%</v-col>
              </v-row>
              <v-row class="predict-row">
                <v-col class="predict-col">Pitch type:</v-col>
                <v-col class="predict-data-col">{{ prediction.type }}</v-col>
              </v-row>
              <v-row class="predict-row">
                <v-col class="predict-col">Speed:</v-col>
                <v-col class="predict-data-col">{{ prediction.speed }} mph</v-col>
              </v-row>
              <v-row class="predict-row">
                <v-col class="predict-col">Location:</v-col>
                <v-col class="predict-data-col">Zone {{ prediction.location }}</v-col>
              </v-row>
          </v-col>
      </v-row>

    </v-card>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'my-component',
  computed: {
    ...mapState({
        pitcherId: state => state.current.pitcher.id,
        prediction: state => state.prediction,
    }),
    imageURL(){

      try {
         return require("@/assets/heat_maps_v2/" + this.prediction.img)

      }  catch (error){
          console.error('Error loading image URLs:', error);
          return require("@/assets/heat_maps_v2/default_heat_map.jpg")
      }
    },
  },
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