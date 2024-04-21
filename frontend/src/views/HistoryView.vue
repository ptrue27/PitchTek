<template>
  <v-container fluid class="history-container">
    <button @click="addComponent">Add Component</button>
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
      'predictions', 'outs', 'balls', 'strikes', 'bases'])
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
        home: this.home,
        away: this.away,
        predictions: this.predictions,
        outs: this.outs,
        balls: this.balls,
        strikes: this.strikes,
        bases: [...this.bases]
      };
      // Push the store snapshot into components array
      this.components.unshift(storeSnapshot);
    }
  }
};
</script>

<style>
.component {
  margin-top: 2px;
  padding: 2px;
  border: 0px solid #ccc;
}

.history-container {
  background-color: #C8E6C9;
  height: auto;
}
</style>
