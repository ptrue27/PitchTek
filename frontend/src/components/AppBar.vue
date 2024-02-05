<template>
    <v-app-bar>
      <v-img
        src="@/assets/baseball-icon.png"
        alt="PitchTek logo"
        max-height="50"
        max-width="50"
        class="ml-5"
        contain
      ></v-img>

      <v-app-bar-title>PitchTek</v-app-bar-title>

      <v-btn
        to="/about"
        prepend-icon="mdi-view-dashboard"
        variant="tonal" class="mr-5"
      >
        About
      </v-btn>

      <v-btn
        to="/dashboard"
        prepend-icon="mdi-view-dashboard"
        variant="tonal" class="mr-5"
      >
        Dashboard
      </v-btn>

      <v-btn
        to="/statistics"
        prepend-icon="mdi-magnify"
        variant="tonal" class="mr-5"
      >
        Statistics
      </v-btn>

      <v-btn
        to="/history"
        prepend-icon="mdi-history"
        variant="tonal" class="mr-2"
      >
        History
      </v-btn>

    </v-app-bar>
</template>
<script setup>
</script>