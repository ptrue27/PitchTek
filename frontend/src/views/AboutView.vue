<template>
    <v-container fluid class="history-container">
      <!-- Single Row for all components -->
      <v-row>

        <v-col cols="12"> <!-- This takes the full width -->
          <Prediction />
        </v-col>

        <v-col cols="12"> <!-- This takes the full width -->
          <Prediction />
        </v-col>

      </v-row>
    </v-container>
</template>

<style>


</style>

<script>
import Prediction from "@/components/PreviousPrediction.vue"

export default {
  components: {
    Prediction
  }
}
</script>