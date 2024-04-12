<template>
  <v-app>
    <AppBar />
      <v-main>
        <router-view  class="app-container" v-slot="{ Component }">
            <keep-alive>
              <component :is="Component"></component>
            </keep-alive>
        </router-view>
      </v-main>
  </v-app>
</template>

<script setup>
  import AppBar from "./components/AppBar.vue"
</script>

<style>
.app-container {
  min-height: 100%;
}
</style>