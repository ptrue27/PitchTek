<template>
    <v-container fluid class="dashboard-container">
      <v-row>
        <!-- Left Column -->
        <v-col cols="6">
          <v-row>
            <RecordGame />
          </v-row>
          <v-row>
            <ViewPredictions />
          </v-row>
        </v-col>
  
        <!-- Right Column -->
        <v-col cols="6">
          <v-row>
            <PitcherStats />
          </v-row>
          <v-row>
            <MatchupStats />
          </v-row>
          <v-row>
            <BatterStats />
          </v-row>
        </v-col>

      </v-row>
    </v-container>
</template>

<style>
.dashboard-container {
  background-color: rgb(98, 189, 98);
}
</style>

<script>
import RecordGame from "@/components/RecordGame.vue"
import ViewPredictions from "@/components/ViewPredictions.vue"
import PitcherStats from "@/components/PitcherStats.vue"
import MatchupStats from "@/components/MatchupStats.vue"
import BatterStats from "@/components/BatterStats.vue"

export default {
    components: {
    RecordGame,
    ViewPredictions,
    PitcherStats,
    MatchupStats,
    BatterStats,
  }
}
</script>