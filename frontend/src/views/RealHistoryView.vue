<template>
  <div id="app">
    <h1>Previous Predictions</h1>
    <form @submit.prevent="">

    </form>
    <div>
      <ItemComponent
        v-for="(team, index) in teams"
        :key="index"
        :teamName="team.teamName"
        :score="team.score"
      />
    </div>
  </div>
</template>

<script>
import ItemComponent from '@/components/PreviousPrediction2.vue';

export default {
  components: {
    ItemComponent
  },
  data() {
    return {
      teams: [],
      newTeam: {
        teamName: '',
        score: ''
      }
    }
  },
  mounted() {
      this.emitter.on("UpdateHistory", (pitcher_obj) => {

        console.log("Here100", pitcher_obj)

        this.addTeam(pitcher_obj);

      });
  },
  methods: {
    addTeam(pitcher_obj) {
      this.teams.push({
        teamName: pitcher_obj.pitchType[0],
        score: pitcher_obj.pitcherId
      });


    }
  }
}
</script>

<style>
#app {
  text-align: center;
}

input, button {
  margin: 5px;
}
</style>
