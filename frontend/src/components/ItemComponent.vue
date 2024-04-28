<template>
  <div class="item">
    <h4>{{ teamName }}</h4>
    <p>Score: {{ score }}</p>
  </div>
</template>

<script>
export default {
  props: {
    teamName: String,
    score: String
  }
}
</script>

<style>
.item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-top: 10px;
}
</style>
