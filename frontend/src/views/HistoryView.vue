<template>
  <v-container fluid class="history-container">
    <button @click="addComponent">Add Component</button>
    <div v-for="(component, index) in components" :key="index" class="component">
      <my-custom-component />
    </div>
  </v-container>
</template>

<script>
// Import your custom component
import MyCustomComponent from '@/components/PreviousPrediction.vue';

export default {
  components: {
    MyCustomComponent // Register your custom component
  },
  data() {
    return {
      components: []
    };
  },
  methods: {
    addComponent() {
      this.components.push({});
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
  height: 80px;
}
</style>
