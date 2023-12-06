<script setup>
  import AppBar from "./components/AppBar.vue"
</script>

<template>
  <v-app>
    <AppBar />
      <v-main>
      <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component"></component>
          </keep-alive>
      </router-view>
      </v-main>
  </v-app>
</template>