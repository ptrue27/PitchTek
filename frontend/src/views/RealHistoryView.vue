<template>
  <div>
    <button @click="addComponent">Add Component</button>
    <div v-for="(component, index) in components" :key="index" class="component">
      <my-custom-component />
    </div>
  </div>
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
  margin-top: 10px;
  padding: 10px;
  border: 1px solid #ccc;
}
</style>
