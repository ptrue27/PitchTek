<template>
  <div class="page-background">
    <div v-for="(component, index) in components" :key="index" class="component">
      <my-custom-component />
    </div>
  </div>
</template>

<script>
// Import your custom component
import MyCustomComponent from '@/components/PreviousPrediction2.vue';

export default {
  components: {
    MyCustomComponent // Register your custom component
  },
  mounted() {
      this.emitter.on("UpdateHistory", pitcher_obj => {

        console.log("AAAAAAAAAAAAAAAAAAA", pitcher_obj)
        this.AddLog();

      });
  },
  data() {
    return {
      components: []
    };
  },
  methods: {
    AddLog() {

      this.components.push({});
    }
  }
};
</script>

<style>
.component {
  margin-top: 0px;
  padding: 0px;
  border: 0px solid #ccc;
}
.page-background {
  background-color: #bbb4b4; /* Example color */
}
</style>
