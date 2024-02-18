<template>
  <v-app>
    <v-container>
      <!-- Use v-img with dynamic src binding -->
      <v-img
        :src=imageSrc
        alt="Alternative Text"
        aspect-ratio="2.75"
        contain
      ></v-img>

      <!-- Button to change the image dynamically -->
      <v-btn @click="changeImage">Change Image</v-btn>
    </v-container>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      imageSrc: require("@/assets/FF_heat_map.jpg") // Default image source
    };
  },
  methods: {
    changeImage() {
      // Simulate changing image dynamically
      this.imageSrc = require("@/assets/strikezone.jpg");
    }
  }
};
</script>

<style scoped>
/* Your component-specific styles */
</style>
