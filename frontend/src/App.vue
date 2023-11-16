<script setup>
  import AppBar from "./components/AppBar.vue"
  import DashboardView from "./components/DashboardView.vue"
</script>

<template>
  <v-app>

    <AppBar />

    <v-main>
      <DashboardView />
    </v-main>

  </v-app>
</template>