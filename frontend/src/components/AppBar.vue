<template>
  <v-card>
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
        prepend-icon="mdi-view-dashboard"
        variant="tonal"
        class="mr-5"
      >
        Dashboard
      </v-btn>

      <v-btn
        prepend-icon="mdi-magnify"
        variant="tonal"
        class="mr-5"
      >
        Statistics
      </v-btn>

      <v-btn
        prepend-icon="mdi-history"
        variant="tonal"
        class="mr-5"
      >
        History
      </v-btn>

    </v-app-bar>
  </v-card>
</template>
