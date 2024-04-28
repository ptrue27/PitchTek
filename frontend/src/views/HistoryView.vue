<template>
  <v-container fluid  class="dashboard-container">
    <div v-for="(componentData, index) in components" :key="index" class="component">
      <!-- Pass the store snapshot as a prop to my-custom-component -->
      <my-custom-component :storeSnapshot="componentData" />
    </div>
  </v-container>
</template>

<script>
import MyCustomComponent from '@/components/PreviousPrediction.vue';
import {mapState} from 'vuex';

export default {
  components: {
    MyCustomComponent
  },
  computed: {
    ...mapState(['inning', 'home', 'away',
      'prediction', 'outs', 'balls', 'strikes', 'bases', 'current'])
  },
  data() {
    return {
      components: []
    };
  },
  methods: {
    addComponent() {
      // Capture the entire state of the Vuex store
      const storeSnapshot = {
        inning: this.inning,
        home_name: this.home.teamName,
        home_score: this.home.score,
        away_name: this.away.teamName,
        away_score: this.away.score,
        prediction_img: this.prediction.img,
        prediction_speed: this.prediction.speed,
        prediction_location: this.prediction.location,
        prediction_confidence: this.prediction.confidence,
        prediction_type: this.prediction.type,
        outs: this.outs,
        balls: this.balls,
        strikes: this.strikes,
        base_first: this.bases[0],
        base_second: this.bases[1],
        base_third: this.bases[2],
        pitcher_name: this.current.pitcher.name,
        pitcher_img: this.current.pitcher.img,
        batter_name: this.current.batter.name,
        batter_img: this.current.batter.img,
      };
      // Push the store snapshot into components array
      this.components.unshift(storeSnapshot);
    }
  },
  created() {
    this.emitter.on('UpdateHistory', this.addComponent);
  }
};
</script>

<style>
.component {
  margin-top: 2px;
  padding: 2px;
  border: 0px solid #ccc;
}
</style>
